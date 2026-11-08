---
name: deep-research
description: Run a thorough, source-cited investigation of a topic using web search and fetch, separating evidence from opinion and hype. Use when asked to research, investigate, evaluate a technology or product, do a competitive analysis, or "dig into" a topic beyond a quick answer.
---

# Deep Research

Investigate a topic in depth and return an independent, cited assessment.

## Workflow

1. **Frame the questions.** Restate the topic and list the 3-7 key questions that must be answered. If the scope is unclear, ask the user one clarifying question first.
2. **Search widely.** Use web search with several differently phrased queries per question. Prefer primary sources: official docs, original research, standards, filings, changelogs.
3. **Read the important sources.** Fetch the most relevant pages instead of relying on snippets.
4. **Compare perspectives.** Note where sources agree, disagree, or compete.
5. **Filter quality.** Separate evidence from opinion and marketing. Flag anything outdated (check publish dates).
6. **Synthesize.** Form an independent assessment. Do not just list search results.

## Output format

- **Summary**: 3-5 sentences with the bottom line.
- **Findings**: one section per key question, each claim with an inline link `[source](url)`.
- **Disagreements and open questions**
- **What we know / don't know / should check next**
- **Sources**: list of links used.

## Rules

- Cite every important factual claim.
- Label confidence (high / medium / low) on key conclusions.
- Paraphrase sources; do not copy long passages.
- If web tools are unavailable, say so and stop rather than answer from memory.
