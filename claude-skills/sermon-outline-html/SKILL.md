# sermon-outline-html

Merge a transcript markdown file and its matching `sermon-outline` markdown file into a single self-contained HTML page, styled per the `html-guide-style` skill. Sibling of `transcript-outline-html`, but built for `sermon-outline`'s shape rather than the general `outline` skill's — see "Why a separate skill" below.

## Invocation

```bash
$PYTHON "$CLAUDE_SKILLS_DIR/sermon-outline-html/merge-html.py" <path-to-transcript.md>
$PYTHON "$CLAUDE_SKILLS_DIR/sermon-outline-html/merge-html.py" <path-to-transcript.md> <path-to-sermon-outline.md>
```

If the sermon-outline path is omitted, it's derived from the transcript filename:
```
{id}-{slug}-claude-transcript.md  →  {id}-{slug}-claude-sermon-outline.md
```

Use `--path-only` to print the resolved output path without generating the file.

## Requirements

- Input transcript must be in the format produced by `youtube-transcriber`: a `# Title` heading, a `- **URL:** ...` line, and a `## Transcript` section.
- Input sermon outline must be in the format produced by the `sermon-outline` skill: `# Sermon Outline: {Title}` frontmatter (Source/Preacher/Series/Passage), an Overview, a `## Scripture Referenced` table, an optional `## Greek/Hebrew Word Studies` table, numbered `## N. Title` points (each with an `<!-- anchor: "..." -->` comment, optional excerpt, `**Overview:**`, labeled sub-points, and `**Reflect:**` questions), and a `## Key Takeaways` table.
- No external dependencies — includes its own minimal markdown-to-HTML converter (headers, bold/italic, blockquotes, tables, bullet/numbered lists, horizontal rules, paragraphs).

## Why a Separate Skill (not a `transcript-outline-html` mode)

The two source formats aren't interchangeable enough to share one parser:

1. **Leading-text handling differs.** `transcript-outline-html` backfills any transcript text before the first section's anchor into block 1 — correct when the outline covers the *whole* transcript. `sermon-outline` only covers the sermon, so its first anchor sits well into the transcript, after all the liturgy. This script does **not** backfill leading text — pre-sermon material is excluded entirely, matching `sermon-outline`'s intent.
2. **Extra top-level section.** `sermon-outline` has a `## Scripture Referenced` table between the Overview and the numbered points, which `transcript-outline-html`'s parser has no concept of and would misparse as a broken point.
3. **Richer per-point content.** Points use nested sub-points (`- **Claim:** ...`) and numbered Reflect questions, which needed list support added to the markdown converter — `transcript-outline-html`'s converter deliberately stayed minimal and doesn't have this.

## What Claude Does

1. Run the script against the transcript file (and sermon-outline file, if not co-located under the standard naming convention).
2. The script:
   - Parses the sermon-outline's frontmatter (title, source URL, preacher, series, passage) into header badges.
   - Renders the Overview and Scripture Referenced table as their own top-level sections (not toggle blocks).
   - If present, renders the Greek/Hebrew Word Studies table as its own top-level section, and links each word's first mention inside the point(s) named in its "Used In" column back to its glossary row (see "Glossary Linking" below). The section is omitted entirely — no empty heading — if the sermon outline has no Word Studies table.
   - Uses each point's anchor to slice the transcript into one chunk per point, with no leading-text backfill.
   - Builds one block per point with a Summary/Transcript toggle — the Summary view holds the point's Overview, labeled sub-points, and Reflect questions; the Transcript view holds that point's transcript slice.
   - Renders Key Takeaways (+ conclusion, if present) as the final section.
3. Check stderr for warnings: points missing an anchor, or anchors that couldn't be matched. Fix the sermon outline's anchor and re-run if that happens.
4. Save the output alongside the source files using the naming convention below.

## Output File Naming

```
{id}-{slug}-claude-sermon-outline.md  →  {id}-{slug}-claude-sermon.html
```

## Block Behavior

- Each point becomes one block with its own Summary/Transcript toggle (defaults to Summary), toggled independently per block, same interaction pattern as `transcript-outline-html`.
- Summary view: excerpt (if any), Overview sentence, labeled sub-points as a bullet list, Reflect questions as a numbered list.
- Transcript view: that point's sliced transcript text — starts exactly at the point's anchor, with no preceding service content included.

## Glossary Linking

- The Word Studies table's "Used In" column (e.g. `Point 2` or `Points 2, 4`) drives linking — for each point number listed, the script finds that word's *first* italicized occurrence inside that point's rendered HTML and wraps it in a link to its glossary row.
- Clicking the link jumps to the glossary table and highlights the target row via CSS `:target` — no JavaScript tooltip/pop-up layer, kept deliberately simple (see the skill's design rationale: the `.md` source needs to work as plain markdown too, so the glossary itself is a table, not a hover-only feature; the HTML version's only addition is the jump-link).
- If a word's transliteration doesn't literally appear inside the point's markdown as `*word*` (e.g. the preacher's exact wording varies, or the term was only discussed in **Biblical support** without italics), the link is silently skipped for that mention — the glossary row itself still renders regardless, so no information is lost, only the in-context jump link.

## Integration with Other Skills

- **youtube-transcriber**: produces the source transcript markdown.
- **sermon-outline**: produces the source sermon-outline markdown.
- **transcript-outline-html**: the equivalent tool for the general `outline` skill's output — use that instead when the outline covers the whole service/document, not just a sermon.
- **html-guide-style**: this skill's visual design (dark theme, sidebar, active-section highlighting) follows that style guide.
