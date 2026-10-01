"""Reproduce selected observations at three pinned hotel snapshots.

Exit success means observations were collected, including known defects.
This is a study harness, not an application acceptance suite.
Requires Python 3, Docker, Java 25, and the already-built artifacts.
All database writes use a new disposable PostgreSQL container.
"""
import argparse
import concurrent.futures
import datetime as dt
import http.server
import json
import os
from pathlib import Path
import socket
import subprocess
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

ROOT = None
OUT = None
DB = None


def sql(database, query):
    result = subprocess.run(['docker', 'exec', '-i', DB['name'], 'psql', '-XAt', '-v',
                             'ON_ERROR_STOP=1', '-U', 'postgres', '-d', database],
                            input=query, text=True, capture_output=True, check=True)
    return result.stdout.strip()


def port():
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0))
        return sock.getsockname()[1]


def call(base, method, path, payload=None, headers=None):
    data = None if payload is None else json.dumps(payload).encode()
    request = urllib.request.Request(base + path, data=data, method=method,
                                     headers={'Content-Type': 'application/json', **(headers or {})})
    try:
        response = urllib.request.urlopen(request, timeout=15)
    except urllib.error.HTTPError as error:
        response = error
    raw = response.read()
    return response.status, json.loads(raw) if raw else None


class Upstream(http.server.BaseHTTPRequestHandler):
    rates_up = True
    payments_up = True

    def do_GET(self):
        query = urllib.parse.parse_qs(urllib.parse.urlsplit(self.path).query)
        first = dt.date.fromisoformat(query['start_date'][0])
        last = dt.date.fromisoformat(query['end_date'][0])
        self.reply(200 if self.rates_up else 503,
                   [{'amount_cents': 10000} for _ in range((last - first).days)])

    def do_POST(self):
        self.rfile.read(int(self.headers.get('Content-Length', '0')))
        self.reply(200 if self.payments_up else 503,
                   {'status': 'refunded' if 'refund' in self.path else 'paid'})

    def reply(self, status, value):
        body = json.dumps(value).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *_args):
        pass


def start(binary, database, environment, health):
    listen_port = port()
    logfile = (OUT / (database + '-probe-server.log')).open('w')
    process = subprocess.Popen([str(binary)], cwd='/tmp',
                               env={**os.environ, 'DATABASE_URL':
                                    f"postgres://postgres:study-local-only@127.0.0.1:{DB['port']}/{database}",
                                    'PORT': str(listen_port), 'SERVER_PORT': str(listen_port), **environment},
                               stdout=logfile, stderr=subprocess.STDOUT)
    base = f'http://127.0.0.1:{listen_port}'
    for _ in range(100):
        if process.poll() is not None:
            raise RuntimeError(f'Server exited; inspect {logfile.name}')
        try:
            if call(base, 'GET', health)[0] == 200:
                return process, logfile, base
        except (OSError, urllib.error.URLError):
            pass
        time.sleep(0.1)
    raise RuntimeError('Server did not become ready')


def race(database, lock_query, action):
    holder = subprocess.Popen(['docker', 'exec', '-i', DB['name'], 'psql', '-XAt', '-v',
                               'ON_ERROR_STOP=1', '-U', 'postgres', '-d', database],
                              stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    holder.stdin.write("BEGIN;\n" + lock_query + ";\n")
    holder.stdin.flush()
    while True:
        line = holder.stdout.readline()
        if line.strip() == 'lock_ready':
            break
        if not line:
            holder.communicate(timeout=5)
            raise RuntimeError('Inventory lock failed')
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            futures = [pool.submit(action) for _ in range(2)]
            waiting = 0
            for _ in range(100):
                waiting = int(sql(database, "SELECT count(*) FROM pg_stat_activity WHERE datname=current_database() "
                                  "AND pid<>pg_backend_pid() AND wait_event_type='Lock' AND state='active'"))
                if waiting >= 2:
                    break
                time.sleep(0.05)
            holder.stdin.write('COMMIT;\n')
            holder.stdin.flush()
            if waiting < 2:
                raise RuntimeError('Could not force both cancellations to overlap')
            return [future.result() for future in futures]
    finally:
        holder.communicate('ROLLBACK;\n', timeout=5)


def collect_rust_and_java_probes():
    upstream = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Upstream)
    threading.Thread(target=upstream.serve_forever, daemon=True).start()
    upstream_url = f'http://127.0.0.1:{upstream.server_port}'
    servers = []
    results = {}
    try:
        green = ROOT / 'hotel-rust'
        process, logfile, base = start(green / 'target/debug/reservation-service', 'hr_reservation',
                                      {'RATE_SERVICE_URL': upstream_url, 'PAYMENT_SERVICE_URL': upstream_url}, '/healthz')
        servers.append((process, logfile))
        first = dt.date.today() + dt.timedelta(days=500)
        last = first + dt.timedelta(days=1)
        hotel_id = '00000000-0000-4000-8000-000000000001'
        room_id = '10000000-0000-4000-8000-000000000001'
        booking = {'idempotency_key': str(uuid.uuid4()), 'hotel_id': hotel_id, 'room_type_id': room_id,
                   'guest_name': 'Probe Guest', 'guest_email': 'probe@example.test', 'check_in': str(first),
                   'check_out': str(last), 'room_count': 1, 'payment_method_token': 'test:success'}
        code, saved = call(base, 'POST', '/v1/reservations', booking)
        assert code == 201, (code, saved)
        _, second = call(base, 'POST', '/v1/reservations', {**booking, 'idempotency_key': str(uuid.uuid4())})
        assert second['status'] == 'paid', second
        Upstream.rates_up = False
        results['greenfield_replay_with_rates_down'] = {'http_status': call(base, 'POST', '/v1/reservations', booking)[0],
                                                       'stored_status': saved['status']}
        Upstream.rates_up = True
        results['greenfield_read_without_guest_credentials'] = {'http_status': call(base, 'GET', '/v1/reservations/' + saved['id'])[0]}
        query = f"SELECT 'lock_ready' FROM room_type_inventory WHERE hotel_id='{hotel_id}' AND room_type_id='{room_id}' AND night='{first}' FOR UPDATE"
        replies = race('hr_reservation', query,
                       lambda: call(base, 'DELETE', f"/v1/reservations/{saved['id']}?guest_email=probe%40example.test"))
        remaining = int(sql('hr_reservation', f"SELECT total_reserved FROM room_type_inventory WHERE hotel_id='{hotel_id}' AND room_type_id='{room_id}' AND night='{first}'"))
        results['greenfield_concurrent_cancel'] = {'http_statuses': [r[0] for r in replies], 'expected_reserved': 1, 'actual_reserved': remaining}
        Upstream.payments_up = False
        pending = {**booking, 'idempotency_key': str(uuid.uuid4()), 'check_in': str(first + dt.timedelta(days=2)), 'check_out': str(last + dt.timedelta(days=2))}
        failed_code, _ = call(base, 'POST', '/v1/reservations', pending)
        pending_status = sql('hr_reservation', f"SELECT status FROM reservations WHERE idempotency_key='{pending['idempotency_key']}'")
        results['greenfield_payment_unavailable'] = {'http_status': failed_code, 'stored_status': pending_status}
        Upstream.payments_up = True

        rebuilt = ROOT / 'hotel-dry-kiss-yagni-refactored-ddd-cleanarch-cqrs-rermade-rust'
        process, logfile, base = start(rebuilt / 'services/backend/target/debug/stays-backend', 'rebuilt', {'ADMIN_API_KEY': ''}, '/health')
        servers.append((process, logfile))
        hotel_id = '11111111-1111-1111-1111-111111111111'
        room_id = '10000000-0000-0000-0000-000000000101'
        booking = {'reservationId': str(uuid.uuid4()), 'hotelId': hotel_id, 'roomTypeId': room_id,
                   'guestName': 'Probe Guest', 'guestEmail': 'probe@example.test', 'checkIn': str(first),
                   'checkOut': str(last), 'rooms': 1, 'guests': 2}
        code, saved = call(base, 'POST', '/api/reservations', booking)
        assert code == 200 and saved['status'] == 'CONFIRMED', (code, saved)
        code, second = call(base, 'POST', '/api/reservations', {**booking, 'reservationId': str(uuid.uuid4())})
        assert code == 200 and second['status'] == 'CONFIRMED', (code, second)
        results['rebuilt_read_without_guest_credentials'] = {'http_status': call(base, 'GET', '/api/reservations/' + saved['id'])[0]}
        query = f"SELECT 'lock_ready' FROM reservations.room_inventory WHERE hotel_id='{hotel_id}' AND room_type_id='{room_id}' AND inventory_date='{first}' FOR UPDATE"
        replies = race('rebuilt', query, lambda: call(base, 'DELETE', '/api/reservations/' + saved['id']))
        remaining = int(sql('rebuilt', f"SELECT total_reserved FROM reservations.room_inventory WHERE hotel_id='{hotel_id}' AND room_type_id='{room_id}' AND inventory_date='{first}'"))
        results['rebuilt_concurrent_cancel'] = {'http_statuses': [r[0] for r in replies], 'expected_reserved': 1, 'actual_reserved': remaining}
        code, saved = call(base, 'POST', '/api/reservations', {**booking, 'reservationId': str(uuid.uuid4()), 'guests': 999,
                                                             'checkIn': str(first + dt.timedelta(days=4)), 'checkOut': str(last + dt.timedelta(days=4))})
        results['rebuilt_capacity_validation'] = {'http_status': code, 'requested_guests': 999, 'room_max_guests': 2, 'stored_guests': saved.get('guests')}
        code, _ = call(base, 'PUT', '/api/admin/rates', {'roomTypeId': room_id, 'date': str(first), 'amount': 250}, {'X-Admin-Key': ''})
        results['rebuilt_empty_admin_key'] = {'http_status': code, 'configured_key': 'empty', 'supplied_key': 'empty'}
        results.update(probe_java_architecture())
        (OUT / 'probes.json').write_text(json.dumps(results, indent=2) + '\n')
        print(json.dumps(results, indent=2))
    finally:
        upstream.shutdown()
        for process, logfile in servers:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
            logfile.close()




def probe_java_architecture():
    name = 'hotel-ddd-cleanarch-cqrs'
    jar = ROOT / name / 'services/reservation-service/target/reservation-service-1.0.0.jar'
    listen_port = port()
    log = (OUT / 'java-architecture-server.log').open('w')
    arguments = ['java', '-jar', str(jar), '--server.address=127.0.0.1',
                 f'--server.port={listen_port}',
                 f"--spring.datasource.url=jdbc:postgresql://127.0.0.1:{DB['port']}/java_architecture?currentSchema=hotel_reservation",
                 '--spring.datasource.username=postgres', '--spring.datasource.password=study-local-only']
    process = subprocess.Popen(arguments, cwd='/tmp', stdout=log, stderr=subprocess.STDOUT)
    base = f'http://127.0.0.1:{listen_port}'
    try:
        for _ in range(300):
            if process.poll() is not None:
                raise RuntimeError(f'Java startup failed; inspect {log.name}')
            try:
                if call(base, 'GET', '/actuator/health')[0] == 200:
                    break
            except (OSError, urllib.error.URLError):
                pass
            time.sleep(0.1)
        else:
            raise RuntimeError('Java architecture startup timed out')
        first = dt.date.today() + dt.timedelta(days=150)
        booking = {'hotelId': 'rio-casa-do-mar', 'roomTypeId': 'room-casa-mar-terrace',
                   'guestName': 'Probe Guest', 'guestEmail': 'probe@example.test',
                   'checkIn': str(first), 'checkOut': str(first + dt.timedelta(days=1)),
                   'rooms': 1, 'guests': 2}
        reservations = []
        for _ in range(2):
            code, saved = call(base, 'POST', '/api/reservations', booking,
                               {'Idempotency-Key': str(uuid.uuid4())})
            assert code == 201, (code, saved)
            reservations.append(saved)
        where = f"room_type_id='room-casa-mar-terrace' AND inventory_date='{first}'"
        replies = race('java_architecture',
                       f"SELECT 'lock_ready' FROM hotel_reservation.inventory_days WHERE {where} FOR UPDATE",
                       lambda: call(base, 'DELETE', '/api/reservations/' + reservations[0]['id'] +
                                    '?email=probe%40example.test'))
        available = int(sql('java_architecture',
                            f'SELECT available_rooms FROM hotel_reservation.inventory_days WHERE {where}'))
        return {'java_architecture_concurrent_cancel': {
            'http_statuses': [reply[0] for reply in replies], 'expected_available': 6,
            'actual_available': available, 'physical_capacity': 7}}
    finally:
        process.terminate()
        try:
            process.wait(timeout=8)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
        log.close()


def main():
    global ROOT, OUT, DB
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--projects-root', type=Path, required=True,
                        help='Directory containing the three inspected repositories')
    parser.add_argument('--output-dir', type=Path, required=True,
                        help='Directory for probe output and temporary server logs')
    args = parser.parse_args()
    ROOT, OUT = args.projects_root.resolve(), args.output_dir.resolve()
    OUT.mkdir(parents=True, exist_ok=True)
    snapshots = {
        'hotel-rust': '961071eaa773c6f0e37c438da8336d2ac2f466eb',
        'hotel-ddd-cleanarch-cqrs': '47b0c3b79a96ba94c433e54639bfe9cdc5be1541',
        'hotel-dry-kiss-yagni-refactored-ddd-cleanarch-cqrs-rermade-rust': 'fba23789a507bf3179a214560ee7f215ad9eaa74',
    }
    for name, expected in snapshots.items():
        actual = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT / name, text=True).strip()
        changes = subprocess.check_output(['git', 'status', '--porcelain'], cwd=ROOT / name, text=True)
        if actual != expected or changes:
            raise RuntimeError(f'{name} must be clean and checked out at {expected}')
    binaries = [ROOT / 'hotel-rust/target/debug/reservation-service',
                ROOT / 'hotel-dry-kiss-yagni-refactored-ddd-cleanarch-cqrs-rermade-rust/services/backend/target/debug/stays-backend',
                ROOT / 'hotel-ddd-cleanarch-cqrs/services/reservation-service/target/reservation-service-1.0.0.jar']
    if any(not path.is_file() for path in binaries):
        raise RuntimeError('Build the Rust binaries and Java architecture JAR using the article appendix first')
    DB = {'name': 'hotel-study-' + uuid.uuid4().hex[:12]}
    subprocess.run(['docker', 'run', '--detach', '--rm', '--name', DB['name'],
                    '-e', 'POSTGRES_PASSWORD=study-local-only', '-p', '127.0.0.1::5432',
                    'postgres:17-alpine'], capture_output=True, check=True)
    try:
        for _ in range(60):
            if subprocess.run(['docker', 'exec', DB['name'], 'pg_isready', '-h', '127.0.0.1', '-U', 'postgres'],
                              capture_output=True).returncode == 0:
                break
            time.sleep(0.25)
        else:
            raise RuntimeError('Disposable PostgreSQL did not become ready')
        DB['port'] = subprocess.check_output(['docker', 'port', DB['name'], '5432/tcp'],
                                             text=True).strip().rsplit(':', 1)[1]
        for database in ['hr_reservation', 'rebuilt', 'java_architecture']:
            subprocess.run(['docker', 'exec', DB['name'], 'createdb', '-U', 'postgres', database],
                           capture_output=True, check=True)
        collect_rust_and_java_probes()
    finally:
        subprocess.run(['docker', 'stop', DB['name']], capture_output=True, check=True)


if __name__ == '__main__':
    main()
