# Performance and accessibility checks

The site still builds with Ruby/Bundler. Font subsets are committed. Node and
Python packages are only needed for the specific asset workflows below.
Initialize the pinned theme assets before building a fresh checkout:

```sh
git submodule update --init assets/lib
bash tools/test.sh
```

## Lighthouse

Serve the production build with gzip in one terminal, then audit it in another:

```sh
python3 tools/serve-audit.py
bash tools/lighthouse.sh http://127.0.0.1:4174 /tmp/chirpy-lighthouse
```

The audit script requires Node 22.19+ and Chrome. It uses Lighthouse 13.5.0,
runs all posts sequentially with the default mobile throttling and desktop
preset, and saves JSON and HTML reports. It exits unsuccessfully if any category
scores below 100. Lighthouse scores fluctuate; inspect the underlying metrics
when a run fails. The local server compresses text responses to approximate
production delivery, but does not simulate public hosting latency or cache headers.
Run the script against the public URL after deployment to verify hosted results.

## Diagrams

Write diagrams as Mermaid fences in `_posts`, including their `accTitle` and
`accDescr`. Chirpy renders the fences in the browser using Mermaid from the
pinned `assets/lib` submodule. Mermaid rendering is enabled for posts by default
in `_config.yml`; there are no generated diagram assets to regenerate.

## Fonts and theme updates

To regenerate the local font subsets after changing theme icons or updating Chirpy:

```sh
uv venv /tmp/chirpy-font-tools
uv pip install --python /tmp/chirpy-font-tools/bin/python 'fonttools[woff]==4.62.1'
/tmp/chirpy-font-tools/bin/python tools/subset-fonts.py
```

Body text and headings use the native system font stack, avoiding font downloads
and layout shifts. Font Awesome is subset to the icons found in the theme and
site sources; its modified fonts have new internal names and retain their license.
The theme stylesheet overrides Chirpy's supported font variables.

The build inlines render-blocking CSS and the small theme-mode initializer.
Scripts and font files remain separate cacheable assets. Accessibility fixes
are applied to generated HTML, so they also work without JavaScript. After a
theme update, regenerate fonts, run HTML validation and Lighthouse, and check
mobile navigation, search, code copying, image zoom, and both color schemes.
