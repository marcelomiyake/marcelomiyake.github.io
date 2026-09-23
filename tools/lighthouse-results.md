# Lighthouse results — 2026-09-22

All six posts scored **100 in every category on mobile and desktop** in the final 12-audit run.

Scores below are Performance / Accessibility / Best Practices / SEO. Lighthouse 13.5's Agentic Browsing category also scored 100 for every post in both profiles.

| Post | Baseline mobile | Final mobile | Final desktop |
| --- | --- | --- | --- |
| Prompt Engineering | 56 / 91 / 100 / 100 | 100 / 100 / 100 / 100 | 100 / 100 / 100 / 100 |
| AI Gateways and Model Routing | 38 / 96 / 100 / 100 | 100 / 100 / 100 / 100 | 100 / 100 / 100 / 100 |
| Context Engineering | 43 / 92 / 100 / 100 | 100 / 100 / 100 / 100 | 100 / 100 / 100 / 100 |
| Harness Engineering | 48 / 92 / 100 / 100 | 100 / 100 / 100 / 100 | 100 / 100 / 100 / 100 |
| Spec-Driven Development | 45 / 92 / 100 / 100 | 100 / 100 / 100 / 100 | 100 / 100 / 100 / 100 |
| Loop Engineering | 45 / 92 / 100 / 100 | 100 / 100 / 100 / 100 | 100 / 100 / 100 / 100 |

## What changed

- Replaced client-side Mermaid execution with generated SVGs, keeping editable Mermaid sources, descriptive alt text, explicit dimensions, lazy loading, and image zoom. SVGs have a readable background in dark mode.
- Served theme dependencies locally through the existing pinned assets submodule; enabled submodule checkout in the Pages workflow.
- Used native system fonts for article text and headings, subset Font Awesome to the theme’s icons, and inlined render-blocking styles and the small theme initializer.
- Added accessible heading links, post-navigation names that include visible titles, and labels for contents/back-to-top controls. Improved line-number contrast in both themes and enabled viewport zoom.

## Verification

- Lighthouse **13.5.0**, Chrome **154**, production Jekyll build, cold storage, sequential runs.
- Default mobile simulated throttling (150 ms RTT, 1,638.4 Kbps throughput, 4× CPU slowdown); default desktop preset.
- Both comparison builds served locally with gzip using `tools/serve-audit.py`. The baseline uses the original theme configuration and client-rendered diagrams for these six posts.
- `bash tools/test.sh`: production build and HTML-Proofer passed.
- Browser checks passed for dark mode, code copying, search, mobile navigation, image zoom, both diagrams loading, no horizontal page overflow, and diagrams with JavaScript disabled. No browser or network errors were observed.
- A build under `/preview` also passed HTML-Proofer; inlined stylesheet asset URLs resolved correctly.

## Reproduce and inspect

See [the tooling guide](README.md) for audit and regeneration commands. Raw HTML and JSON reports from this run are in `/tmp/chirpy-lighthouse-system-fonts/`; regenerate them if temporary files are cleared.

These are local production-build measurements, not audits of a deployed update. Hosting latency, cache headers, hardware, and Lighthouse versions can change scores. No commit, push, or deployment was performed.
