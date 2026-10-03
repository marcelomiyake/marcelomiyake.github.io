# Marcelo Masahiko Miyake

My engineering notebook: case studies, design decisions, and experiments in software architecture, distributed systems, and AI-assisted development. The posts show how I approach requirements, compare architectures, and examine implementation behavior, in English and Brazilian Portuguese.

[Visit the Blog](https://marcelomiyake.com.br)

## About Me

I am a Software Engineering Specialist and Systems Architect based in São Paulo, Brazil, with more than 20 years in software engineering and over 13 years at Atech working on mission-critical systems.

Start with the [hotel implementation study](https://marcelomiyake.com.br/posts/five-ai-hotel-implementations/) and its [maintenance follow-up](https://marcelomiyake.com.br/posts/five-ai-hotel-implementations-part-2/). See [About](https://marcelomiyake.com.br/about/) for my background and engineering approach.

To be clear, my goal lately isn't to build production-ready projects on GitHub. Over recent months, I wanted to improve the process for working with AI tools and practices and test whether it is possible to get good results with cheap models. Every project has guardrails for code quality and all of them were deployed on Kubernetes (most repositories feature real screenshots in the cluster), but they probably have plenty of bugs!

You can also find me on:

- [GitHub](https://github.com/marcelomiyake)
- [LinkedIn](https://linkedin.com/in/marcelomiyake)
- [X](https://twitter.com/MarceloMIYAKE)

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
