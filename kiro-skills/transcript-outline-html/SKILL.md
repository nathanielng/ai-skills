---
name: transcript-outline-html
description: Merge a transcript markdown file and its matching outline markdown file into a single self-contained HTML page with a collapsible outline sidebar. Use when asked to combine a transcript and outline into HTML, or to produce a browsable page from a transcript.
---

# transcript-outline-html

Merge a transcript markdown file and its matching outline markdown file into a single self-contained HTML page: the transcript's title and URL become the page header, and the body is broken into per-section blocks (one per outline section) with a Summary/Transcript toggle on each block. A collapsible sidebar holds the overview, a jump-link nav, and the Key Takeaways table.

## Invocation

When the user asks to combine/merge a transcript and outline into HTML, or "make an HTML version of this transcript with the outline as a sidebar."

## Workflow

1. Locate the transcript markdown file (and outline markdown file, if not co-located under the standard naming convention).
2. Run the script:
   ```bash
   python3 ~/.kiro/skills/transcript-outline-html/merge-html.py <path-to-transcript.md> [path-to-outline.md]
   ```
   If the outline path is omitted, it's derived automatically:
   ```
   {id}-{slug}-claude-transcript.md  →  {id}-{slug}-claude-outline.md
   ```
3. The script extracts the title/URL from the transcript header, parses the outline structurally (overview, per-section title/anchor/excerpts/summary, Key Takeaways table), uses each section's anchor snippet to slice the transcript into matching chunks, and builds one toggleable block per section plus a sidebar (overview + nav + Key Takeaways).
4. Check stderr for warnings about missing or unmatched anchors — fix the outline and re-run if needed.
5. Output is saved alongside the source files as `{id}-{slug}-claude.html`.

## Requirements

- Transcript must be in the format produced by the `youtube-transcriber` skill: `# Title` heading, `- **URL:** ...` line, `## Transcript` section.
- Outline must be in the format produced by the `outline` skill, **including an `<!-- anchor: "..." -->` comment under each `## N. Title` heading** (a short verbatim snippet marking where that section starts in the transcript). Without it, that section's transcript view falls back to a placeholder.
- No external dependencies — includes its own minimal markdown-to-HTML converter (headers, bold/italic, blockquotes, tables, horizontal rules, paragraphs). Not a general-purpose renderer.

## Sidebar Behavior

- Open by default: overview text, jump-link nav to each block, and the Key Takeaways table (+ conclusion, if present). Per-section summaries live in the blocks, not the sidebar.
- A "☰ Outline" button toggles it collapsed/expanded.
- Self-contained (inline CSS/JS, no network calls), supports light/dark via `prefers-color-scheme`.

## Block Behavior

- Each outline section becomes one block with its own Summary/Transcript toggle (defaults to Summary), toggled independently per block.
- Summary view: excerpt blockquote(s) (if any) + the section's `**Summary:**` text. Transcript view: that section's sliced transcript text.

## Integration with Other Skills

- **youtube-transcriber**: produces the source transcript markdown.
- **outline**: produces the source outline markdown.
- Run this after both of the above have been generated for a given video.
