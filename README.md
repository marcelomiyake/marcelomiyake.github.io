# Marcelo Masahiko Miyake

Welcome to my corner! Every post here is written by AI, exploring software engineering and life in the AI age. Judge me!

[Visit the Blog](https://marcelomiyake.com.br)

## About Me

I am Marcelo Masahiko Miyake. You can find me on:

- [GitHub](https://github.com/marcelomiyake)
- [LinkedIn](https://linkedin.com/in/marcelomiyake)
- [Twitter](https://twitter.com/marcelomiyake)

## Credits

This blog is built with [Jekyll](https://jekyllrb.com/) and the [Chirpy](https://github.com/cotes2020/jekyll-theme-chirpy) theme.

## Develop locally

The site uses Ruby and Bundler. Use the Ruby version in `.ruby-version`, initialize the pinned theme assets in a fresh checkout, and install the locked dependencies:

```sh
git submodule update --init assets/lib
bundle install
```

Start a local preview:

```sh
bash tools/run.sh
```

For the production-mode preview, use `bash tools/run.sh --production`. To rebuild the production site and check its generated HTML, run:

```sh
bash tools/test.sh
```

This script replaces the generated `_site` directory and runs HTMLProofer without checking external links. See [AGENTS.md](AGENTS.md) for repository guidance and [tools/README.md](tools/README.md) for diagram, font, and Lighthouse workflows.

## Publishing

GitHub Actions builds and deploys the site to GitHub Pages after a qualifying push to `main` or `master`; it can also be started manually from the Actions tab. A local build does not publish the site. README-only changes are excluded from the automatic deployment workflow.
