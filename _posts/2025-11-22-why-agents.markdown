---
layout: post
title: "Why Every Project Needs AGENTS.md"
date: 2025-11-22 00:00:00 -0300
categories: ai agents amzonq
---

# Why Every Project Needs AGENTS.md

## The Problem: README.md Isn't Enough for AI Agents

While `README.md` serves as excellent documentation for human developers, AI agents often require different context and instructions. Human developers intuitively understand their environment, but AI agents need explicit guidance about:

- Shell environment quirks
- Tool-specific execution patterns
- Project-specific conventions
- Deployment procedures
- Integration points

## The Solution: AGENTS.md

The `AGENTS.md` file (or `.amazonq/rules/AGENTS.md` for Amazon Q) provides **agent-specific context** that complements human-readable documentation.

### Industry Recognition

This pattern is gaining traction in the software development community:

- **Thoughtworks Technology Radar** featured [AGENTS.md](https://www.thoughtworks.com/en-br/radar/techniques/agents-md) as an emerging technique for AI-assisted development
- **agents.md** initiative ([https://agents.md/](https://agents.md/)) promotes standardization of agent context files across tools and platforms

## Key Differences: README.md vs AGENTS.md

| Aspect       | README.md                     | AGENTS.md                                    |
| ------------ | ----------------------------- | -------------------------------------------- |
| **Audience** | Humans (and AI)               | AI Agents exclusively                        |
| **Content**  | Architecture, features, setup | Execution patterns, tool quirks, automation  |
| **Commands** | Standard shell commands       | Agent-specific wrappers (e.g., `bash -i -c`) |
| **Focus**    | Understanding the system      | Operating the system                         |
| **Examples** | Conceptual examples           | Executable commands                          |

## Real-World Example: Shell Environment

### The Problem

Human developers can execute commands directly:

```bash
mvn clean install
kubectl get pods
npm run build
```

But AI agents (like Amazon Q) run in non-interactive shells where environment variables aren't loaded. The common workaround `source ~/.bashrc` fails because `.bashrc` typically exits early with:

```bash
[ -z "$PS1" ] && return
```

### The Solution in AGENTS.md

```markdown
## Shell Environment

**IMPORTANT:** When executing bash commands that require environment variables, use interactive shell mode:

bash -i -c "mvn clean install"
bash -i -c "kubectl get pods"
bash -i -c "npm run build"
```

**Why:** The `source ~/.bashrc` approach fails in non-interactive shells.

This instruction is **irrelevant for humans** but **critical for AI agents**.

## What Should Go in AGENTS.md?

### 1. Tool Execution Patterns

```markdown
## Build Commands

bash -i -c "mvn clean install"
bash -i -c "npm run build"
```

### 2. Environment-Specific Context

```markdown
## Kubernetes Contexts

- dev: https://dev.example.com
- staging: https://staging.example.com
- prod: https://prod.example.com

Check current context:
bash -i -c "kubectl config current-context"
```

### 3. Critical Conventions

```markdown
## Database Migrations

**CRITICAL:** All migration files MUST follow:
YYYYMMDDHHMM\_\_TICKET-XXXX_description.sql

**MUST be current timestamp when creating**
```

### 4. Integration Points

```markdown
## Message Queue Topics

**Publisher:**

- service-name.entity.created
- service-name.entity.updated

**Subscriber:**

- other-service.event.occurred
- external-service.data.changed
```

### 5. Automation Workflows

```markdown
## Code Quality

After coding, ALWAYS run:
bash -i -c "npm run lint"
bash -i -c "npm test"
```

### 6. Security Requirements

```markdown
## API Authentication

**CRITICAL:** All new API endpoints MUST include authentication.
Add @PreAuthorize annotation or configure in security rules.
```

## Benefits of AGENTS.md

### 1. **Reduced Friction**

Agents don't need repeated instructions for environment-specific quirks.

### 2. **Consistency**

All agents (Amazon Q, GitHub Copilot, Cursor, etc.) receive the same context.

### 3. **Long-Term Context**

Instructions persist across sessions without cluttering prompts.

### 4. **Separation of Concerns**

- `README.md` → Human understanding
- `AGENTS.md` → Agent execution

### 5. **Onboarding Efficiency**

New team members using AI tools get immediate, accurate guidance.

### 6. **Convention Enforcement**

Critical patterns (naming, commits, migrations) are automatically followed.

## Implementation Strategies

### Option 1: Root-Level (Universal)

```
project-root/
├── AGENTS.md          # For all AI tools
├── README.md
└── ...
```

### Option 2: Tool-Specific (Amazon Q)

```
project-root/
├── .amazonq/
│   └── rules/
│       └── AGENTS.md  # Amazon Q specific
├── README.md
└── ...
```

### Option 3: Hybrid

```
project-root/
├── AGENTS.md          # Universal patterns
├── .amazonq/
│   └── rules/
│       └── AGENTS.md  # Amazon Q overrides
├── README.md
└── ...
```

## Best Practices

### 1. Be Explicit

❌ "Build the project"
✅ `bash -i -c "mvn clean install"`

### 2. Include Context

```markdown
## Database

**Connection:** postgres:5432
**Database:** myapp_db
**Schema:** public
```

### 3. Highlight Critical Patterns

Use **CRITICAL** or **IMPORTANT** for non-negotiable requirements.

### 4. Provide Examples

Show actual commands, not just descriptions.

### 5. Keep It Updated

Treat AGENTS.md as living documentation alongside code changes.

### 6. Link Related Resources

```markdown
## API Documentation

- dev: https://dev.example.com/api/docs
- staging: https://staging.example.com/api/docs
```

## When to Use AGENTS.md vs README.md

### Use README.md for:

- Architecture overview
- Feature descriptions
- Conceptual explanations
- Human setup instructions
- Contribution guidelines

### Use AGENTS.md for:

- Executable commands
- Environment quirks
- Tool-specific patterns
- Automation workflows
- Critical conventions
- Integration details

## Adoption Checklist

- [ ] Create `AGENTS.md` or `.amazonq/rules/AGENTS.md`
- [ ] Document shell environment requirements
- [ ] List all executable commands with proper wrappers
- [ ] Define critical naming conventions
- [ ] Map integration points (APIs, message queues, databases)
- [ ] Include environment-specific URLs and credentials
- [ ] Document automation workflows
- [ ] Add security requirements
- [ ] Link to related services
- [ ] Test with actual AI agent interactions

## Conclusion

`AGENTS.md` bridges the gap between human intuition and AI agent execution. As AI-assisted development becomes standard practice, providing explicit agent context is no longer optional—it's essential for productive, error-free automation.

By separating human-focused documentation (`README.md`) from agent-focused instructions (`AGENTS.md`), projects can serve both audiences effectively without compromise.

## References

- [Thoughtworks Technology Radar - AGENTS.md](https://www.thoughtworks.com/en-br/radar/techniques/agents-md)
- [agents.md Initiative](https://agents.md/)
- [Amazon Q Developer Documentation](https://docs.aws.amazon.com/amazonq/)

---

**Start using AGENTS.md today and watch your AI-assisted development workflow transform from frustrating to frictionless.**
