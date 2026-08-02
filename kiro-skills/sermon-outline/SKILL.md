---
name: sermon-outline
description: Church-specific outline generator that covers only the sermon/message portion of a service transcript (skipping liturgy, announcements, offering, etc.), with labeled sub-points per point, a scripture cross-reference table, and reflection questions. Use for church service transcripts when only the sermon content matters, not the full service.
---

# sermon-outline

Church-specific sibling of the general `outline` skill. Generates an in-depth outline of **only the sermon/message portion** of a church service transcript — skipping call to worship, announcements, offering, testimonies, commissioning, and other liturgical elements. Where `outline` produces a broad, lighter-touch recap of a whole document, `sermon-outline` goes deep on a single sermon: labeled sub-points per section, a scripture cross-reference table, and reflection questions.

## When to Use

Use `sermon-outline` instead of `outline` when the source is a church service transcript and the sermon itself — not the surrounding service — is what matters. Use plain `outline` for everything else (including transcripts where you want the *whole* service recapped, e.g. for a "what happened at church" summary rather than a study aid).

## Workflow

1. Read the source transcript (or use content already in context).
2. Identify where the sermon/message begins and ends, distinguishing it from liturgical elements (call to worship, announcements, offering, testimonies, commissioning, prayers, benediction, etc.). Judge this from the content itself — sermons are usually introduced by name ("this morning's message," a series title, the preacher being introduced) and organized around a passage and points, not service flow. **Everything outside that boundary is left out of this outline entirely** — it is not a lighter summary of the rest of the service, it's simply not covered. If the transcript is ambiguous about where the sermon starts, err toward including slightly more rather than less, and note the uncertainty in the Overview.
3. Write a sermon-only outline with:
   - A frontmatter block including the primary passage/text and series name, if known.
   - An Overview of the sermon (not the whole service).
   - A **Scripture Referenced** table listing every passage cited in the sermon (not just the primary text), each with a one-line note on how it's used.
   - A **Greek/Hebrew Word Studies** table, if the preacher does any original-language word studies — one row per word, see below. Omit the whole section if the sermon has none.
   - Numbered points, each with: an anchor comment, optional excerpt(s), a short **Overview** sentence, then labeled sub-points, then 1–2 **Reflect** questions.
   - A final **Key Takeaways** table.
4. **Run a mandatory verification pass** before saving (see "Verification Pass" below) — this is not optional, and is the step most responsible for catching content the first draft misses.
5. Save the output to the same directory as the source file using the naming convention below.

## Output File Naming

```
{id}-{slug}-claude-transcript.md  →  {id}-{slug}-claude-sermon-outline.md
```

Distinct from the general `outline` skill's `-claude-outline.md` — the two can coexist for the same video if you want both a full-service recap and a sermon-only deep dive.

## Point Structure

For each sermon point:

```markdown
## N. Point Title

<!-- anchor: "verbatim snippet from the start of this point in the transcript" -->

[Optional excerpt(s) — see "Excerpts: Scan Actively" below. Not just "include if obviously quotable."]

**Overview:** 1–2 sentence digest of the point — what it's about, in brief.

- **Claim:** The core assertion of this point, stated plainly.
- **Biblical support:** The verse(s)/exegesis used to ground the claim — cite specific references and note original-language points (Greek/Hebrew word studies) if the preacher makes them.
- **Illustration:** The story, example, or analogy used, if any — summarized, not transcribed.
- **Application:** What the preacher asks the congregation to do or examine as a result of this point.
- **Notable Citations:** Anything cited that isn't the preacher's own claim, a Bible verse, or a personal-story illustration — historical documents/artifacts, statistics, quotes from other authors or works, named external sources. See below; this is the label most likely to be forgotten, and forgetting it is exactly the failure mode it exists to prevent.

**Reflect:**
1. A question testing understanding or inviting personal reflection on this point.
2. A second question, if a second angle is genuinely useful — skip rather than pad.
```

Not every sub-point label applies to every point — omit any that have no real content (e.g. a point might have no distinct "Illustration" or "Notable Citations"). Never fabricate content to fill a label. This is deliberately more granular and longer per-point than the general `outline` skill: aim for the sub-points combined to cover meaningfully more ground than a single 2–5 sentence summary would.

### Notable Citations: Why This Label Exists

Bible verses go in **Biblical support**. Personal stories, analogies, and testimonies go in **Illustration**. Everything else the preacher cites to support a point — a historical document or artifact, a statistic, a quote from a book/covenant/other author, a named external source — has nowhere else to go, and without an explicit label for it, it's easy to drop silently rather than force it into a category it doesn't fit. If a point has one of these, it goes under **Notable Citations**; if it doesn't, omit the label rather than leaving it empty.

### Excerpts: Scan Actively

Don't wait for an excerpt to jump out. Before finalizing each point, explicitly ask: does this point's transcript slice contain a named source, a specific statistic, or a quoted document/author distinct from scripture? If yes, either pull it as an excerpt or capture it under **Notable Citations** (an excerpt if the exact wording is worth preserving verbatim; **Notable Citations** if a paraphrase is enough). The old "include a quote if it's strong and quotable" framing only catches material that's already obviously punchy — it misses citations that matter for content reasons even when the wording itself isn't quotable.

## Scripture Referenced Table

Right after the Overview, before the numbered points:

```markdown
## Scripture Referenced

| Passage | Used For |
|---|---|
| 1 Thessalonians 1:5–10 | Primary text for this week's message |
| James 2:22, 26 | Supporting faith-produces-works argument in Point 1 |
```

Include the primary passage and every passage quoted or alluded to, in the order first referenced. One line each — this is a lookup table, not a commentary.

## Greek/Hebrew Word Studies Table

Right after Scripture Referenced, before the numbered points — only include this section if the sermon actually does original-language word studies (many do, some don't):

```markdown
## Greek/Hebrew Word Studies

| Word | Language | Meaning | Used In |
|---|---|---|---|
| *ergon* (ἔργον) | Greek | "work," related to "energy" — action, not mere mental assent | Point 2 |
| *kopos* (κόπος) | Greek | labor to the point of exhaustion | Point 3 |
```

- **Word**: the transliteration in italics, with the original script in parentheses if the preacher gave it (don't guess the original script if they only said the transliteration).
- **Meaning**: the preacher's own gloss/definition, not an independent lexicon lookup — this documents what was taught, not an external scholarly claim.
- **Used In**: the point number(s) where it appears, e.g. `Point 2` or `Points 2, 4`. This is load-bearing, not decorative — `sermon-outline-html` uses it to link each word's first mention in the point text back to its glossary row.
- A word that's already fully explained inline within a point's **Biblical support** doesn't need to also appear here in full — but every original-language word study the preacher does should have a row, even a short one, so the sermon's full set of word studies is visible at a glance in one place rather than scattered across points.

## Key Takeaways Table

Identical convention to the `outline` skill — 5–10 rows, standalone insights, placed at the end.

## Verification Pass (Mandatory)

A first draft reliably captures a sermon's main argument but reliably misses secondary supporting material — the first pass is built around Claim/Biblical support/Illustration/Application, and anything that doesn't fit one of those labels tends to just get left out rather than flagged. Do not skip this step.

After drafting the full outline, do a second read of each point's transcript slice (the text between its anchor and the next point's anchor) specifically hunting for anything not yet reflected anywhere in that point — not the argument, which the first pass gets right, but the supporting detail around it:

- A named document, artifact, historical event, or other external source
- A specific number, date, or statistic
- A quote from someone other than the preacher or the scripture passage itself
- A Greek/Hebrew word study not yet in the Word Studies table

If you find one that isn't already captured, add it under **Notable Citations**, as an excerpt, or as a Word Studies row (see above), before finalizing. If a point genuinely has none, move on — the point of this pass is to catch omissions, not to manufacture content.

## Full Output Template

```markdown
# Sermon Outline: {Sermon Title}

**Source:** {file path or URL}
**Preacher:** {if known}
**Series:** {series name, if part of one}
**Passage:** {primary text for this sermon}

---

{Overview of the sermon specifically — 2-4 sentences}

---

## Scripture Referenced

| Passage | Used For |
|---|---|
| ... | ... |

---

## Greek/Hebrew Word Studies

| Word | Language | Meaning | Used In |
|---|---|---|---|
| ... | ... | ... | ... |

---

## 1. First Point Title

<!-- anchor: "..." -->

> "Excerpt, if strong."

**Overview:** ...

- **Claim:** ...
- **Biblical support:** ...
- **Illustration:** ...
- **Application:** ...
- **Notable Citations:** ...

**Reflect:**
1. ...

## 2. Second Point Title

[... same structure ...]

---

## Key Takeaways

| # | Takeaway |
|---|----------|
| 1 | ... |

---

{Conclusion, if the sermon builds to a distinct closing charge/application beyond its final point}
```

## Options

- `--no-excerpts` — Skip quoted excerpts, keep everything else.
- `--no-reflect` — Skip the Reflect questions (e.g. if this is for personal reference rather than group study).

## Python Helper

```bash
python3 ~/.kiro/skills/sermon-outline/sermon-outline.py /path/to/transcript.md
```

Same behavior as `outline`'s helper: prints the source file to stdout and resolves the correct output path.

## Integration with Other Skills

- **youtube-transcriber**: produces the source transcript.
- **outline**: use instead of (or alongside) this skill when you want the whole service covered, not just the sermon.
- **transcript-outline-html**: currently expects the `outline` skill's `-claude-outline.md` naming and section-summary format; it does not yet support `sermon-outline`'s output directly. Treat that as a possible future extension rather than assuming it works today.
