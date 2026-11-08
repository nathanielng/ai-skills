---
name: review-work
description: Expert review of existing work (code, designs, reports, proposals, plans) for correctness, gaps, clarity, and failure modes, then an improved version. Use when asked to review, critique, check, or improve a file, document, design, or piece of code.
---

# Review Work

Review the user's work as an experienced subject-matter expert. Explain problems before rewriting.

## Workflow

1. **Get the work.** Read the file(s) or text the user points to. For code, also read nearby files to learn conventions, and run existing tests or linters if available.
2. **Identify the goal.** State in one line what the work is meant to do. If unclear, ask.
3. **Evaluate** against:
   1. Correctness and completeness
   2. Logical consistency
   3. Clarity and structure
   4. Missing considerations
   5. Inefficiency and unnecessary complexity
   6. Failure modes (for code: edge cases, security, error handling)
4. **Report findings first.** For each issue: location, problem, why it matters, recommended fix. Order by severity (high / medium / low).
5. **Then improve.** Provide the improved version. For files, ask before editing unless the user already asked for fixes.

## Rules

- Do not rewrite everything automatically. Findings come first.
- Keep fixes scoped to the issues found. No unrequested refactors.
- Say what is already good, briefly, so it is not changed.
