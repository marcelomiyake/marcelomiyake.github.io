# Repository Guide

This repository contains Marcelo Miyake's Jekyll blog, built with the Chirpy theme. Posts live in `_posts`, site pages in `_tabs`, and reusable site tooling in `tools/`. Run commands from the repository root. See `README.md` for project setup and `tools/README.md` for asset regeneration and performance workflows.

## Environment

- Use the Ruby version in `.ruby-version` (currently 3.3.12) and install dependencies with `bundle install`.
- Initialize the pinned theme assets in a fresh checkout with `git submodule update --init assets/lib`.
- The regular site build uses Ruby and Bundler. Node and Python are only needed for specific asset-generation workflows documented in `tools/README.md`.

## Run and validate

- Local preview: `bash tools/run.sh`
- Production-mode preview: `bash tools/run.sh --production`
- Build and validate the production site: `bash tools/test.sh`

`tools/test.sh` removes and rebuilds the generated `_site` directory, then runs HTMLProofer with external-link checks disabled. Do not keep source files or other user data in `_site`. Use the focused commands in `tools/README.md` when changing generated diagrams, fonts, or performance-related code.

## Change guidance

- Keep changes within the requested scope. Inspect the relevant source, scripts, and existing working-tree changes before editing; preserve unrelated user changes.
- Follow [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) for commit messages, using the `<type>[optional scope]: <description>` format and the specification's rules for bodies, footers, and breaking changes.
- Keep SonarQube clear of issues by resolving existing findings as well as any introduced by the change.
- Avoid code duplication by reusing existing implementations or extracting shared behavior.
- For content or behavior changes, use the request or a separate specification for the goal, constraints, out-of-scope cases, and observable acceptance criteria. Keep task-specific plans out of this evergreen guide.
- Prefer the repository scripts as the authoritative commands; update this guide when ongoing setup or workflow instructions change.
- Run checks relevant to the change when requested or needed. In your report, name the commands actually run, their results, and any checks you could not run or cases they do not cover. Do not describe a build as a deployment.

## Publishing

GitHub Actions publishes to GitHub Pages when a qualifying change is pushed to `main` or `master`; the workflow can also be started manually from the Actions tab or with `gh workflow run pages-deploy.yml --ref main` (use `master` if that is the deployment branch). The workflow builds the site, runs HTMLProofer, and deploys the artifact. Commits that change only `README.md` are excluded by the workflow's path filter.

Publishing changes the public site. Push a deployment-triggering commit or dispatch the workflow only when the task explicitly asks to publish. Do not infer publishing authorization from a request to edit, build, test, or commit.
