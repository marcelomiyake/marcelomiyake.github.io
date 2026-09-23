---
layout: post
title: "Prompt Engineering for Developers: Writing Clear Instructions for AI"
seo_title: "Prompt Engineering for Developers | Marcelo Miyake"
date: 2026-09-17 00:00:00 -0300
categories: [Engineering]
tags: [prompt-engineering, ai, llm, coding, best-practices]
description: "Learn how to write effective AI coding prompts with explicit scope, relevant context, testable acceptance criteria, and systematic evaluation."
---

When you tell an AI coding assistant to "build a login screen," you leave critical architectural and product decisions open: which UI framework to use, how authentication tokens are stored, how error states appear, and what actually counts as finished. The model will fill those gaps with reasonable guesses, but those guesses often fail to match your production codebase.

**Prompt engineering** for developers is the discipline of structuring instructions, technical context, and constraints so an AI assistant can produce code that fits the task and codebase. Clearer prompts reduce ambiguity, but the resulting code still needs review and verification.

This is the first guide in a six-part series on AI coding agents—systems that can read repository files, execute terminal tools, and propose validated code changes. The series covers:

1. **Prompt Engineering** (this guide): Writing clear, testable instructions.
2. [AI Gateways and Model Routing]({% post_url 2026-09-18-ai-gateway-routing %}): Directing requests and enforcing policies.
3. [Context Engineering]({% post_url 2026-09-19-context-engineering %}): Feeding the right repository knowledge to agents.
4. [Harness Engineering]({% post_url 2026-09-20-harness-engineering %}): Providing safe tools, sandboxes, and execution environments.
5. [Spec-Driven Development]({% post_url 2026-09-21-spec-driven-development %}): Planning architectures before writing code.
6. [Loop Engineering]({% post_url 2026-09-22-loop-engineering %}): Automating feedback with tests and runtime validation.

Throughout the series, we use a realistic running example: **adding a discount code to an e-commerce checkout flow**.

---

## Four elements of a useful coding prompt

Every effective coding prompt contains four core elements:

### 1. Goal and scope

Define exactly what behavior you want and where the boundary of the change lies. 

* **Weak prompt:** "Improve the checkout page."
* **Strong prompt:** "Prevent duplicate order submissions when users click the checkout button multiple times."

For complex features, ask the agent to inspect the codebase first and propose a plan divided into small, reviewable steps. Assigning a role (such as "Senior TypeScript Engineer") can slightly adjust the tone or perspective, but a persona never replaces concrete requirements, boundaries, or missing technical facts.

### 2. Relevant context

Point the model directly to the files, contracts, and patterns it must follow.

* Name the exact files: the existing implementation, a similar working feature, and the relevant API schema.
* When reporting bugs, paste the exact command executed, the full stack trace, and the environment details.

If your agent has repository tools (such as file search and directory listing), instruct it to inspect specific files before editing. If you are using a standard chat interface without tool access, provide the relevant code snippets directly. Never expect a model to guess private internal APIs or unwritten team conventions.

### 3. Constraints and expected behavior

State all technical and architectural constraints upfront:

* Target runtime and language version (e.g., Node.js 22, Python 3.12).
* Allowed libraries and forbidden dependencies (e.g., "Use existing utilities; do not add external npm packages").
* Public interfaces and backward-compatibility rules.

Describe observable behavior rather than subjective adjectives like "fast," "clean," or "robust." For instance: "If the client submits the same idempotency key twice, return the cached HTTP 200 response without charging the payment gateway again."

### 4. Acceptance criteria and delivery format

Acceptance criteria tell the agent what defines success. Delivery format specifies how to present the answer.

* **Acceptance criteria:** "All existing unit tests pass, and new tests cover empty input, expired tokens, and network timeouts."
* **Delivery format:** "Show a unified git diff followed by a summary of files changed, commands run, and test results."

Keeping these two requirements separate prevents the model from writing code that satisfies the formatting request while quietly skipping validation.

---

## Example: make a validation policy explicit

Consider this common, underspecified developer request:

```text
Write a function that validates emails in TypeScript.
```

This prompt fails to define the input type, whitespace handling, internationalized domain names, or error reporting. Asking for a "fully compliant RFC 5322 regex" usually produces an unreadable 2,000-character regular expression that still misses business edge cases.

In a real application, you want an explicit, testable product policy:

```text
Task: Add an isValidEmail(input: unknown): boolean function as a named export.

Context:
- Inspect existing validation utilities in src/utils/validation.ts.
- Reuse the project's Jest test runner and TypeScript configuration.

Product policy:
- Return false for non-string inputs (null, undefined, numbers, objects).
- Reject empty strings and any leading, trailing, or internal whitespace. Do not trim.
- Local part: Allow only ASCII letters, digits, dots (.), underscores (_), plus signs (+), and hyphens (-).
- Local part: Must not start or end with a dot, and cannot contain consecutive dots (..).
- Domain part: Require exactly one '@' symbol and at least two non-empty domain labels.
- Domain labels: Must contain only ASCII letters, digits, and hyphens, and cannot start or end with a hyphen.
- Network: Reject all other characters. Do not perform DNS or network lookups.

Acceptance test examples:
- Valid (true): "alex@example.com", "alex+shop@sub.example.com"
- Invalid (false): null, 42, "", " alex@example.com", "alex..lee@example.com", "alex@localhost", "alex@-example.com"

Delivery:
- Implement the function in src/utils/validation.ts and add tests in src/utils/validation.test.ts.
- Run the test suite and verify that all edge cases pass.
- Output the changed files, executed commands, test output, and any remaining assumptions.
```

With this prompt, any engineer or automated tool can immediately compare the generated code against unambiguous, verifiable criteria.

---

## Common mistakes in coding prompts

Avoid these frequent pitfalls when working with AI coding tools:

* **Conflicting instructions:** Asking for "concise code with no explanations" while also demanding "detailed rationale for every architectural trade-off." Decide which output you need.
* **Oversized task scope:** Asking an assistant to "refactor the entire billing service to microservices." Break large efforts into small, reviewable increments with intermediate check-ins.
* **Missing edge-case examples:** Bullet points describing rules are helpful, but concrete input/output examples communicate boundaries far more reliably.
* **Treating generation as verification:** A well-written code explanation is not proof of working software. Always run linters, type checkers, and test suites.
* **Premature architectural complexity:** Requesting "Clean Architecture with CQRS, Event Sourcing, and Repository patterns" for a simple CRUD endpoint creates massive maintenance debt. Unless the system already uses those patterns, stick to the simplest solution that meets the requirements. Learn more about this in our guide on [Spec-Driven Development]({% post_url 2026-09-21-spec-driven-development %}#cheap-scaffolding-can-create-expensive-maintenance).

---

## Which language should I use? {#which-language-should-i-use}

Use the natural language in which you can express technical nuance and domain requirements most clearly. You do not need to translate your thoughts into English before talking to an AI model.

If you are developing for a Brazilian team or audience, write in **Brazilian Portuguese (pt-BR)**. You can write your instructions in Portuguese while keeping variable names, SQL queries, API contracts, JSON keys, and error logs in their original English technical form.

### Benchmark evidence and token trade-offs

Model capabilities can vary slightly across languages, but the gap has closed dramatically. In OpenAI's [zero-shot MMLU evaluation](https://cdn.openai.com/gpt-4-5-system-card-2272025.pdf), the o1 model scored **92.3% in English** and **89.5% in Brazilian Portuguese**. This 2.8 percentage-point difference reflects broad general knowledge questions; it does not mean English is strictly superior for domain-specific programming tasks.

However, token consumption does differ. Because most tokenizers are optimized around English text, non-English languages typically require more tokens for the same sentence:

* **English:** *"Please explain how the number of input tokens affects the context window and API cost."* (16 tokens with OpenAI `o200k_base`)
* **Brazilian Portuguese:** *"Explique como a quantidade de tokens de entrada afeta a janela de contexto e o custo da API."* (21 tokens with OpenAI `o200k_base`)

In this case, the Portuguese sentence consumes approximately 31% more tokens. While this slightly increases input cost and context usage, clarity of domain logic always trumps micro-optimizing token counts. For mission-critical prompts, compare both languages side-by-side using identical context and automated tests. See our deep-dive in [Context Engineering]({% post_url 2026-09-19-context-engineering %}#language-coverage-training-data-and-token-budgets) for details on token budgets.

---

## Revise a prompt around an observed failure {#revise-a-prompt-around-an-observed-failure}

Let us apply these principles to our running e-commerce checkout feature.

Suppose your initial request was simply: *"Add discount code support to checkout."*

The agent returns code that calculates discounts entirely inside the client's browser JavaScript and saves the original full price to the database. Instead of adding vague emotional instructions ("Make sure it's secure!"), identify the missing domain ownership rule and revise the prompt:

```text
Task: Add optional discount code support to the checkout flow.

Context:
- Locate the current pricing contract in services/pricing/contracts.
- Trace the quote flow through web storefront, order-service, and pricing-service.

Expected behavior:
- Pricing Service owns eligibility validation and calculation; web storefront only displays the quote.
- Order Service persists the accepted quote ID and final amounts directly from Pricing Service.
- If no discount code is provided, preserve current checkout behavior exactly.
- If an invalid or expired code is entered, display the error returned by Pricing Service and block order placement.

Verification:
- Derive edge-case tests from these rules and the pricing contract.
- Test quote display and database persistence end-to-end.
- Report all executed tests, uncovered edge cases, and unresolved assumptions.
```

By explicitly assigning responsibilities between services, you eliminate the root cause of the architectural defect.

---

## Reuse a working example and a decision record

As Rahul Garg highlights in [Patterns for Reducing Friction in AI-Assisted Development](https://martinfowler.com/articles/reduce-friction-ai/), onboarding an AI assistant with concrete codebase examples dramatically cuts down on iteration time.

Before asking an agent to write new code, ask it to orient itself:

```text
1. Find an existing checkout feature in the repository that follows our current architecture.
2. Identify the route handler, pricing client, and test fixtures by file path.
3. Explain which conventions apply to discount codes and where differences are required.
4. Flag any conflicts with the pricing API contract before making changes.
5. Record confirmed decisions and open questions in docs/decisions/checkout-discounts.md.
```

Giving the assistant an established reference implementation ensures that naming conventions, error handling styles, and test structures remain consistent across the codebase.

---

## Improve prompts with evidence

Prompt engineering should be treated like software engineering: versioned, tested, and evaluated against objective metrics. Follow the methodology outlined by Chip Huyen in *AI Engineering* ([Chapter 5, "Prompt Engineering"](https://www.oreilly.com/library/view/ai-engineering/9781098166298/ch05.html) and [Chapter 3, "Evaluation Methodology"](https://www.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html)):

1. **Prepare test cases:** Create scenarios for valid codes, expired codes, missing codes, and pricing mismatches.
2. **Create benchmark sets:** Use one set of cases to refine Prompt A into Prompt B. Reserve a separate, held-out set of cases for unbiased evaluation.
3. **Run controlled evaluations:** Execute Prompt A and Prompt B using clean git checkouts, identical model parameters, identical tool permissions, and fixed budgets.
4. **Measure complete metrics:** Track pass rates, regression count, repair iterations, review time, latency, and total token cost.

Record each run in an evaluation matrix. The values below are illustrative, not measured results:

| Task / Starting Commit | Prompt & Model Version | Acceptance Tests Passed | Regressions | Repair Iterations | Review Time (min) | Latency (sec) | Total Billed Cost |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Checkout discount #482 | Prompt v1 / Claude 3.5 | 4 / 5 | 1 | 2 | 12 min | 45s | \$0.042 |
| Checkout discount #482 | Prompt v2 / Claude 3.5 | 5 / 5 | 0 | 0 | 4 min | 28s | \$0.028 |

For scalable evaluation, use structured scoring tools such as [TypeSafe Jev's Score primitive](https://docs.typesafe.ai/primitives/score) to grade requirement coverage, verification rigor, and diff clarity, combining results through a [composite scoring pattern](https://docs.typesafe.ai/patterns/composite-scoring).

---

## Summary and next steps

Writing effective prompts is the foundational skill for working with AI coding agents:

* Anchor every prompt with clear **goals, relevant context, strict constraints, and testable acceptance criteria**.
* Provide concrete input/output examples rather than descriptive adjectives.
* Write in your native language, keeping code identifiers in English.
* Evaluate prompt changes systematically with reproducible benchmarks.

Clear instructions tell the model *what* to do. In the next guide, [AI Gateways and Model Routing]({% post_url 2026-09-18-ai-gateway-routing %}), we explore how platform infrastructure routes prompts to the best model while managing cost, latency, and security guardrails.
