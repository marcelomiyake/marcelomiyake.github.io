---
layout: post
title: "Back to the Future: How AI Agents are Reviving Waterfall (but better)"
date: 2025-11-26 00:00:00 -0300
categories: ai agents waterfall agile software-development
---

When ChatGPT was first released, it felt like magic. We used it for quick fixes, explaining regex, or generating boilerplate code. It was a "Chat" experience—reactive and helpful, but limited. It scared the world with possibilities, yet it struggled to execute complex, multi-step tasks or manage large projects autonomously.

Then came the Agents.

With the rise of the Model Context Protocol (MCP) and autonomous agentic workflows, AI has graduated from a chat window to a capable junior developer that lives in our IDEs. It can execute actions, create files, and build entire features. But this new power has revealed a hidden truth: **AI is forcing us back to the drawing board—literally.**

Think about how we delegate to a human junior developer. We often skip details, assuming they'll figure it out or come back with questions later. It's a slow, forgiving feedback loop. The junior works for a few hours, hits a gap, and asks for clarification.

![Junior Developer Feedback Loop](/assets/img/junior_developer_loop.png)

AI collapses this loop. Because it executes at lightning speed, it hits those gaps immediately. It either fails instantly or, worse, confidently builds the wrong thing in seconds. We realize much faster that we missed important details. This "fast failure" forces us to be more complete and precise upfront, effectively front-loading the planning phase just like we used to do.

![Senior Developer Planning for AI](/assets/img/senior_developer_planning.png)

## The "Context" is King

We are finding that to get the best out of these agents, we have to treat them differently than human peers. We are spending more time writing `README.md`, `AGENTS.md`, and detailed technical specifications than ever before. Why?

Because of the **Context Window**.

AI models, no matter how advanced, rely on a finite "working memory" (context window). While modern models boast 1M+ token windows, the "Garbage In, Garbage Out" principle is amplified at scale. If you feed an agent a vague request, you get a vague, often broken, result. But if you feed it structured, precise documentation, the output is exponentially better.

This has made documentation—often the neglected stepchild of Agile development—critical again. These markdown files are the "context" we inject into the agent's brain every time we start a task. The more detailed the map, the better the agent navigates.

## The Rise of "Reasoning" Models

The shift is further accelerated by new "reasoning" models like OpenAI's **o1**. Unlike standard LLMs that predict the next word immediately, these models pause to "think." They generate hidden "reasoning tokens" to break down a problem, plan a path, and verify their logic before writing a single line of code.

This "thinking time" is effectively the **Design Phase** of the Waterfall methodology, compressed into seconds or minutes.

## Plan Mode: The Economic Argument

You mentioned a key pain point: *"Every time we have to explain again and again until AI meets our expectations, we spend time and money."*

This is the economic driver of this shift. In the world of AI development, **iterations are expensive**. Every retry consumes tokens and, more importantly, developer attention.

To minimize this effort, we are seeing the emergence of "Plan Mode" in AI tools. We use the AI to plan the task, split it into detailed subtasks, and architect the solution *before* execution begins.

Does this sound familiar? It should. It sounds a lot like **Waterfall** or **RUP (Rational Unified Process)**—methodologies where we created extensive artifacts before writing the first line of code.

## Micro-Waterfall: The Hybrid Reality

Are we admitting that Waterfall was better than Agile? Not exactly.

Agile gained traction because it improved communication between clients and developers, allowing for flexibility and rapid feedback. That human-to-human dynamic hasn't changed.

However, the **Developer-to-Agent** dynamic is different. An AI agent is the ultimate "literal" worker. It doesn't have the intuition to fill in the gaps of a vague user story. It needs a specification.

We are entering a "Micro-Waterfall" era. Within the broader Agile scope of a project, the individual tasks are being executed with Waterfall-like rigor:
1.  **Requirements**: Detailed `AGENTS.md` and prompts.
2.  **Design**: AI "Plan Mode" or reasoning phase.
3.  **Implementation**: AI code generation.
4.  **Verification**: Human review.

![Micro-Waterfall Process Diagram](/assets/img/micro_waterfall_process.png)

## Conclusion

AI is indeed changing the world, but perhaps not in the way we expected. It's not just automating code; it's enforcing discipline. It's making us plan (or review plans) more than we have in years.

We aren't abandoning Agile, but we are re-learning the value of a well-defined plan. In a twist of irony, the most futuristic technology we have is teaching us that the "old ways" of structured engineering might have been right all along—at least when your teammate is a machine.
