# Homepage and repository presentation review

Reviewed on October 4, 2026. Scope: the public blog homepage, this blog checkout, the `marcelomiyake/marcelomiyake` profile README, and the automation PoC used by the new article. This is an editorial and source review, not a complete audit of every public repository. The presentation recommendations below remain proposals. The accompanying article change includes the pagination metadata fix described under verification; the profile and solver repositories were not edited.

## Highest priority: reconcile public and local presentation

The public blog is hosted at <https://marcelomiyake.com.br/>; this checkout's `_config.yml` and `CNAME` use that domain. Use it consistently in reader-facing links. The repository name remains `marcelomiyake.github.io`.

The public homepage inspected in the in-app browser shows **“AI Engineering & Software Architecture”**, a sidebar description beginning **“Every post here is written by AI”**, and six posts dated September 17–22. The local checkout at `8c695db6fbaba4d87cbfb80b74b15679f4d8b164` already contains **“How I approach software engineering”**, a bilingual introduction, three selected case studies, later posts, and custom thumbnail work.

The public page therefore did not reflect this checkout at review time. This observation does not identify whether the difference comes from the published revision, deployment status, or cached delivery. Inspect the latest Pages workflow and deployed revision before commissioning another homepage redesign. Publishing requires a separate explicit request under `AGENTS.md`.

## Blog homepage and blog repository

| Priority | Finding | Suggested change | Observable acceptance |
| :--- | :--- | :--- | :--- |
| High | The local introduction and selected studies already explain the engineering approach much better than the public page inspected. | Validate and, when publication is requested, deliver the existing local presentation. | Public English and Portuguese pages show the reviewed introduction and selected studies; canonical and language links remain correct. |
| Medium | The selected studies focus on hotel correctness, maintenance, and interactive AI coding. The new solver article adds a distinct scheduled automation example. | Add or rotate in one selected-study entry pointing to `/posts/ai-task-automation/`, using the same bilingual data structure. | Both languages include a concise link explaining scheduled execution and verifiable completion. No separate duplicated layout is introduced. |
| Medium | The blog README is useful for setup but mixes the introduction with a long general disclaimer about production readiness and Kubernetes deployment. | Keep a short statement of experiment scope, then move operational evidence to the relevant project records. Avoid a blanket “all projects” deployment claim. | A visitor can identify the blog's purpose, a starting article, and local setup commands without reading project-wide reliability claims. |
| Medium | The new article connects naturally to the existing harness and loop series. | Keep its contextual links and consider a short “scheduled automation example” link from the older posts when maintaining that series. | Readers can move between the conceptual posts and the working PoC in both languages. |
| Medium | In the local Portuguese article preview at approximately 1266 × 712, the longer sidebar tagline overlaps the first navigation item. This text and sidebar layout predate the new article. | Shorten the Portuguese tagline or let the sidebar introduction grow with its content. Check desktop, mobile navigation, and both languages. | Tagline and navigation remain visually separate at the reviewed size and narrower widths. |

The existing local homepage structure is a good foundation. Reusing `_data/profile.yml` and `_includes/home-intro.html` is sufficient for a new selected case; a layout rewrite is unnecessary.

## GitHub profile repository: `marcelomiyake/marcelomiyake`

The profile README already links to the solver, the hotel studies, the Rust/Vue template, and the notification system. Its table explains why each example matters, and the professional background supports the engineering focus.

1. **Make project scope precise.** The introductory statement that “all of these projects” were deployed on Kubernetes is too broad when the featured work includes this GitHub Actions solver. Narrow it to the application demos that have deployment evidence. Describe the solver as an Actions workflow.
2. **Shorten repeated qualification.** The opening paragraphs, the paragraph after the project table, and the AI authorship section repeat experimental status and limits. Keep one short scope statement near the top and project-specific evidence in the table or linked documentation. This gives the featured work more room without removing the disclosure.
3. **Connect implementation and explanation.** Add the new article's canonical URL beside the existing solver repository link after publication. Suggested wording: “Daily AI automation — [pipeline] · [case study]: scheduled execution, bounded repairs, quality gates, and persistent progress.”
4. **Make Portuguese access explicit.** The profile is English and says work is shared in both languages. Add a small link to the Portuguese blog or the Portuguese version of the featured case study. A second full README translation is optional.

## Solver repository: documentation and behavior to improve

Source snapshot: [`bed6b909c38bb285d11c78ad316dc1faf0f9848f`](https://github.com/marcelomiyake/autonomous-rust-leetcode-solver-pipeline/tree/bed6b909c38bb285d11c78ad316dc1faf0f9848f). Six entries are recorded in `state/progress.json`; recent daily dispatches on October 2–4 succeeded. The source supports a bounded Cargo repair loop and SonarQube Cloud gating before direct publication. It does not implement Jira routing or pull request delivery.

| Priority | Finding | Suggested change |
| :--- | :--- | :--- |
| High | `AGENTS.md` still says the repository has no solutions and describes solution pull requests and merge-gated progress, while the workflow directly publishes existing solutions to `main`. | Update the evergreen project-state and delivery guidance to match current source. Preserve the actual credential and input requirements. |
| High | The README describes public examples and generated tests, but readers can still interpret “verified solutions” as LeetCode judge acceptance. | State prominently that local tests and quality gates are the acceptance scope; no hidden-test verdict is obtained. Add independently maintained regression or property tests if stronger correctness claims are desired. |
| High | `check-models` checks the catalog, is not called by the daily workflow, and cannot verify free-tier billing eligibility. Its warning points to `.github/workflows/solve.yml`, which is not the actual solver workflow. | Correct the path and availability claims. Centralize model configuration before adding a maintenance check. Test retirement, unavailable fallback, and quota exhaustion separately; keep replacements within an explicit billing policy. |
| Medium | The README architecture diagram routes source/output filter failures into repair, but the workflow's repair steps respond only to Cargo validation failures. | Correct the diagram or deliberately add bounded output-contract repair. Distinguish model/API failure, parse failure, local validation failure, and quality-gate failure in reports. |
| Medium | The README calls the filters “lexical and AST validation”; source inspection shows pattern filtering, masking, and a custom structural check for `impl Solution`, rather than a general Rust AST parser. | Describe the actual mechanism and its limits. Avoid presenting it as complete containment of candidate code. |
| Medium | Publication may rebase onto a newer `main` after validation, without repeating checks against that changed base. | Validate the final tree after a rebase that changes the tested base, or publish a branch for CI and review. Preserve progress consistency on failure. |
| Medium | The scheduler can accept a dispatch while the later job fails; the annual fallback is not a daily recovery strategy. | Add a completion-oriented health record or alert for missing/failed expected daily work. Include task identifier, attempt count, actual model, elapsed time, terminal outcome, and published commit. |
| Medium | Jev difficulty is a useful recorded judgment but is not a tested solver eligibility classifier. | If adding issue routing, use explicit supported categories and sufficiency questions, evaluate on labeled issue outcomes, and keep authorization rules in code. |

## Technical details retained in the new posts

- The daily target is 04:17 UTC / 01:17 São Paulo, using cron-job.org to dispatch GitHub Actions.
- The checked job uses `ubuntu-latest` without an explicit job container. Gemini and Jev are remote APIs.
- Gemini returns a structured candidate; public examples inform model-generated tests.
- Jev assesses difficulty; it does not make challenges harder or authorize solver attempts.
- Cargo validation allows two repairs after the initial candidate. A failed output contract or Sonar gate stops the run.
- Model fallback exists, but automatic free-tier model migration has not been demonstrated.
- Jira-to-PR automation is a proposed extension, distinct from this repository's direct-to-main delivery.
- Provider pricing is dated and linked; local overnight hours do not automatically match a provider's off-peak windows.

## Evidence and verification scope

Reviewed the three local repositories with clean working trees before editing. Inspected the public blog in the in-app browser and retrieved the solver's recent Actions history with `gh api`. Read the current primary documentation for [GitHub scheduling](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule), [Gemini models](https://ai.google.dev/gemini-api/docs/models), [Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing), [TypeSafe System One](https://docs.typesafe.ai/concepts/system-one), [TypeSafe confidence](https://docs.typesafe.ai/confidence), and [DeepSeek pricing](https://api-docs.deepseek.com/quick_start/pricing/).

The SonarQube project search for `marcelomiyake.github.io` returned no project. No blog Sonar analysis result is claimed. The solver's configured gate was inspected in source; no new solver run, paid API call, deployment, or repository mutation was performed there.

This report lives under `tools/`, which is excluded from Jekyll output.

### Verification of the accompanying change

- `bundle check`: passed with the installed Ruby 3.3.12 and locked dependencies. Bundler reports a pre-existing deprecation warning about Windows platform names in the Gemfile.
- Initial `bash tools/test.sh`: Jekyll built successfully and HTMLProofer passed; the SEO check failed because adding an eleventh post created `/page2/` with a duplicated homepage description.
- Fixed the new pagination boundary using the existing localized profile data and metadata hook. Paginated index pages now have distinct localized titles and descriptions, canonical URLs, language alternate URLs, Open Graph URLs, and JSON-LD URLs. The first page retains its introduction metadata.
- Final `bash tools/test.sh`: passed theme compatibility, production build, HTMLProofer, and SEO checks for **108 HTML pages**. HTMLProofer checked 377 internal links and internal hashes in 26 files; external-link checks are disabled by the repository script.
- `ruby -c _plugins/seo-metadata.rb` and `git diff --check`: passed.
- Targeted `bundle exec ruby -rnokogiri -rjson -e ...` assertions: passed canonical, Open Graph, JSON-LD, and pagination alternate URL checks on the first and second index pages in both languages.
- Local preview command: `python3 tools/serve-audit.py --directory _site --port 4178`. Inspected English and Portuguese articles in the browser, switched languages, and confirmed both Mermaid diagrams rendered with localized accessibility titles and descriptions. The browser inspection identified the existing Portuguese sidebar overlap noted above.

No full Lighthouse run, mobile viewport audit, solver generation run, model retirement simulation, or hidden LeetCode judge submission was performed. The new article links to dated primary sources, but the production validation command does not recheck those external URLs. No commit, push, workflow dispatch, or deployment was performed for this change.
