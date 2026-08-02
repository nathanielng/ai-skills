---
name: outline
description: Generate a structured outline with key takeaways and optional excerpts from any text content — transcripts, articles, papers, or documents. Use when asked to outline, summarize with structure, extract key points from a file, or create a study guide from content.
---

# Outline

Generate a structured outline with key takeaways and optional excerpts from any text content — transcripts, articles, papers, or documents.

## Invocation

When the user asks to outline a file, or says "outline this", "create an outline of...", etc.

## Workflow

1. Read the source file (or use content already in context)
2. Resolve the output path using the naming convention below
3. Identify the main sections/topics organically from the content
4. Write a structured outline with:
   - An opening framing element (abstract, summary, or conclusion — see rules below)
   - Numbered sections, each with 1–2 optional excerpts and a per-section summary (length scales with section length — see below)
   - A final **Key Takeaways** table summarizing the whole piece
5. Save the output to the same directory as the source file

## Output File Naming

If the source file has the pattern `{id}-{slug}-claude-transcript.txt`, save as:
```
{id}-{slug}-claude-outline.md
```

Otherwise derive from the source filename:
```
{source-filename-without-extension}-outline.md
```

## Framing Element: Abstract vs Summary vs Conclusion

Include **exactly one** of the following, chosen based on the content type:

| Type | Use when | Placed |
|------|----------|--------|
| **Abstract** | Academic papers, research, technical specs — reader needs context *before* diving in | Top, before sections |
| **Summary** | Factual/informational content (interviews, news, how-to, explainers) — recap what was covered | Top, before sections |
| **Conclusion** | Argumentative, opinion, or narrative content — content builds toward a stance or resolution | Bottom, after Key Takeaways |

Default to **Summary** when in doubt.

## Section Structure

For each main section:

```markdown
## N. Section Title

<!-- anchor: "first few words of this section, copied verbatim from the source" -->

> "Direct quote or key excerpt — only if the source has strong quotable passages.
> Skip excerpts for sections where content is dry, list-based, or not quotable."

**Summary:** 2–5 sentences distilling the point of this section, scaled to the section's length —
2–3 sentences for a short section, 3–5 for a longer one. Excerpts are never a substitute for this;
include the summary even when an excerpt is also present.
```

Excerpts are optional per section — use judgment. Prefer quality over quantity. Skip excerpts if the content is tabular, a list of steps, or otherwise doesn't have quotable prose. The per-section summary is not optional.

### Anchors

Every section must include an `<!-- anchor: "..." -->` HTML comment directly under its heading: a short (5–12 word) snippet copied **verbatim, exact substring** from the source text, marking where that section begins. It's invisible when the outline is read as markdown/rendered — its only purpose is letting downstream tooling (e.g. `transcript-outline-html`) locate section boundaries in the original source. Pick a snippet unlikely to repeat elsewhere in the source (avoid generic phrases like "and so" or "thank you").

## Key Takeaways Table

End every outline (before the Conclusion, if one is used) with:

```markdown
## Key Takeaways

| # | Takeaway |
|---|----------|
| 1 | ... |
| 2 | ... |
```

Aim for 5–10 rows. Each row should be a standalone, actionable or memorable insight — not just a label for a section. This table is the terse, cross-section synthesis; it's fine for it to compress or echo points already made in the fuller per-section summaries above.

## Full Output Template

```markdown
# Outline: {Title}

**Source:** {file path}
**Speaker/Author:** {if known}

---

{Abstract or Summary — omit label if Conclusion is used instead}

---

## 1. First Section Title

<!-- anchor: "verbatim snippet from the start of this section" -->

> "Direct quote if available and strong."

**Summary:** 2–5 sentences, scaled to section length.

## 2. Second Section Title

<!-- anchor: "verbatim snippet from the start of this section" -->

> "Quote."

**Summary:** 2–5 sentences, scaled to section length.

[... more sections ...]

---

## Key Takeaways

| # | Takeaway |
|---|----------|
| 1 | ... |

---

{Conclusion — only if argumentative/narrative content}
```

## Options

- `--no-excerpts` — Skip all excerpts, produce a leaner outline with just section titles and summaries.

## Integration with Other Skills

- **youtube-transcriber**: Outline a freshly saved transcript.
- **save-learnings**: After outlining, save key insights to Obsidian.
- **pdf-to-markdown**: Convert a PDF first, then outline the result.
- **web-to-markdown**: Convert a web page, then outline it.
