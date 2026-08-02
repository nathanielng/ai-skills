# transcript-outline-html

Merge a transcript markdown file and its matching outline markdown file into a single self-contained HTML page: the transcript's title and URL become the page header, and the body is broken into per-section blocks (one per outline section) with a Summary/Transcript toggle on each block. A collapsible sidebar holds the overview, a jump-link nav, and the Key Takeaways table.

## Invocation

```bash
$PYTHON "$CLAUDE_SKILLS_DIR/transcript-outline-html/merge-html.py" <path-to-transcript.md>
$PYTHON "$CLAUDE_SKILLS_DIR/transcript-outline-html/merge-html.py" <path-to-transcript.md> <path-to-outline.md>
```

If the outline path is omitted, it's derived from the transcript filename using the `youtube-transcriber`/`outline` naming convention:
```
{id}-{slug}-claude-transcript.md  →  {id}-{slug}-claude-outline.md
```

Use `--path-only` to print the resolved output path without generating the file.

## Requirements

- Input transcript must be in the markdown format produced by the `youtube-transcriber` skill: a `# Title` heading, a `- **URL:** ...` line, and a `## Transcript` section containing the body.
- Input outline must be in the format produced by the `outline` skill (headings, blockquote excerpts, `**Summary:**` lines, a Key Takeaways table) **and must include an `<!-- anchor: "..." -->` comment under each `## N. Title` heading** — a short verbatim snippet from the transcript marking where that section begins. Without an anchor, the script can't locate that section's boundary in the transcript and its transcript view will show a "could not locate" placeholder instead of the real excerpt.
- No external dependencies — the script includes its own minimal markdown-to-HTML converter (headers, bold/italic, blockquotes, tables, horizontal rules, paragraphs). It is not a general-purpose markdown renderer; it only needs to handle the subset of markdown these two skills produce.

## What Claude Does

1. Run the script against the transcript file (and outline file, if not co-located under the standard naming convention).
2. The script:
   - Extracts the title and URL from the transcript's header.
   - Parses the outline structurally: the opening overview text, each numbered section (title, anchor, excerpts, summary), and the Key Takeaways table (+ conclusion, if present).
   - Uses each section's anchor snippet to locate its start in the transcript and slices the transcript into one chunk per section, in document order.
   - Builds one block per outline section: a heading, a Summary/Transcript toggle, a summary view (excerpts + summary text) and a transcript view (that section's transcript slice) — only one view visible at a time, toggled independently per block.
   - Builds the sidebar from the overview text, a jump-link nav to each block, and the Key Takeaways table/conclusion.
3. Check stderr for warnings: sections missing an anchor comment, or anchors the script couldn't find in the transcript (usually because the snippet was paraphrased rather than copied verbatim). Fix the outline's anchor and re-run if that happens.
4. Save the output alongside the source files using the naming convention below.

## Output File Naming

```
{id}-{slug}-claude-transcript.md  →  {id}-{slug}-claude.html
```

Example: `MwHJLSOU3PU-12-july-2026-...-claude-transcript.md` → `MwHJLSOU3PU-12-july-2026-...-claude.html`

## Sidebar Behavior

- The sidebar is open by default and contains the overview text, a jump-link nav to each section block, and the Key Takeaways table (+ conclusion, if present). It does not repeat the per-section summaries — those live in the blocks themselves.
- A "☰ Outline" button in the top-left collapses/expands the sidebar via a CSS class toggle (no external JS libraries).
- The page is self-contained (inline CSS/JS, no network requests) and supports both light and dark viewing via `prefers-color-scheme`.

## Block Behavior

- Each outline section becomes one block in the main content area with its own "Summary" / "Transcript" toggle (pill-style buttons), defaulting to the Summary view.
- Toggling is independent per block — you can have some sections showing their summary and others showing raw transcript at the same time.
- The Summary view shows the section's excerpt blockquote(s) (if any) plus its `**Summary:**` text. The Transcript view shows that section's sliced transcript text.

## Integration with Other Skills

- **youtube-transcriber**: produces the source transcript markdown.
- **outline**: produces the source outline markdown.
- Run `/transcript-outline-html` after both of the above have been generated for a given video.
