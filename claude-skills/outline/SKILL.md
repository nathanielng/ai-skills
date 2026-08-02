# outline

Generate a structured outline with key takeaways and optional excerpts from any text content — transcripts, articles, papers, or documents.

## Invocation

```
/outline <path-to-file>
/outline <path-to-file> --no-excerpts
```

Or when content is already in the conversation context (e.g., a transcript was just generated), invoke `/outline` with no arguments and Claude will use the most recently loaded content.

## What Claude Does

When this skill is invoked, Claude:

1. Reads the source file (or uses content already in context)
2. Identifies the main sections/topics organically from the content
3. Writes a structured outline with:
   - An opening framing element (abstract, summary, or conclusion — see rules below)
   - Numbered sections, each with 1–2 optional excerpts and a per-section summary (length scales with section length — see below)
   - A final **Key Takeaways** table summarizing the whole piece
4. Saves the output to the same directory as the source file using the naming convention below

## Output File Naming

If the source file has the pattern `{id}-{slug}-claude-transcript.txt`, save as:
```
{id}-{slug}-claude-outline.md
```

Otherwise derive a slug from the source filename:
```
{source-filename-without-extension}-claude-outline.md
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

[1–2 direct quotes or key excerpts — only include if the source text has strong quotable passages.
 Skip excerpts entirely for sections where the content is dry, list-based, or not quotable.
 Excerpts should be indented block-quotes.]

**Summary:** 2–5 sentences distilling the point of this section, scaled to the section's length —
2–3 sentences for a short section, 3–5 for a longer one. Excerpts are never a substitute for this;
include the summary even when an excerpt is also present.
```

Excerpts are optional per section — use judgment. Prefer quality over quantity: a section with one strong excerpt is better than two weak ones. Skip excerpts if the content is tabular, a list of steps, or otherwise doesn't have quotable prose. The per-section summary is not optional.

**Order is fixed and there is no other prose in a section**: heading → anchor comment → excerpt(s), if any → `**Summary:**` line. Never add a framing sentence before the excerpt/summary, and never put the excerpt after the summary — everything the section says must live inside the excerpt blockquote(s) and the one `**Summary:**` paragraph, nothing else.

### Anchors

Every section must include an `<!-- anchor: "..." --> ` HTML comment directly under its heading: a short (5–12 word) snippet copied **verbatim, exact substring** from the source text, marking where that section begins. It's invisible when the outline is read as markdown/rendered — its only purpose is letting downstream tooling (e.g. `transcript-outline-html`) locate section boundaries in the original source. Pick a snippet unlikely to repeat elsewhere in the source (avoid generic phrases like "and so" or "thank you").

## Key Takeaways Table

End every outline (before the Conclusion, if one is used) with a markdown table:

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

**Source:** {file path or URL}
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

## Python Helper

The `outline.py` script reads a source file and prints its contents to stdout, so Claude can process it without a separate Read tool call. It also resolves the correct output path.

```bash
$PYTHON "$CLAUDE_SKILLS_DIR/outline/outline.py" /path/to/transcript.txt
```

Output is printed to stdout; Claude then generates the outline and saves it using the Write tool.

## Integration with Other Skills

- **youtube-transcriber**: Run `/outline` immediately after `/youtube-transcriber` to outline the freshly saved transcript.
- **save-learnings**: After outlining, use `/save-learnings` to save key insights to Obsidian.
- **pdf-to-markdown**: Convert a PDF first, then `/outline` the result.
