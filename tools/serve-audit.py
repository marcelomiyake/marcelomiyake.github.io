#!/usr/bin/env python3
"""Serve a production build with gzip, as GitHub Pages does (no warm cache)."""
import argparse
import gzip
import io
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer


class Handler(SimpleHTTPRequestHandler):
    def send_head(self):
        path = self.translate_path(self.path)
        from pathlib import Path
        file = Path(path)
        if file.is_dir() and self.path.endswith('/'):
            file = file / 'index.html'
        if file.is_file() and file.suffix in {'.html', '.css', '.js', '.json', '.svg', '.xml'} and 'gzip' in self.headers.get('Accept-Encoding', ''):
            data = gzip.compress(file.read_bytes())
            self.send_response(200)
            self.send_header('Content-Type', self.guess_type(str(file)))
            self.send_header('Content-Encoding', 'gzip')
            self.send_header('Vary', 'Accept-Encoding')
            self.send_header('Content-Length', str(len(data)))
            self.end_headers()
            return io.BytesIO(data)
        return super().send_head()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', default='_site')
    parser.add_argument('--port', type=int, default=4174)
    args = parser.parse_args()
    ThreadingHTTPServer(('127.0.0.1', args.port), partial(Handler, directory=args.directory)).serve_forever()
