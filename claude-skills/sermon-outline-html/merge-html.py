#!/usr/bin/env python3
"""
Transcript + Sermon Outline -> HTML merger.

Combines a `{id}-{slug}-claude-transcript.md` file and its matching
`{id}-{slug}-claude-sermon-outline.md` file (from the `sermon-outline` skill)
into a single self-contained HTML page, styled per the `html-guide-style`
skill. Unlike `transcript-outline-html` (which pairs with the general
`outline` skill), this expects the sermon-outline shape: a frontmatter block
(Preacher/Series/Passage), an Overview, a Scripture Referenced table, numbered
points (each with Overview + labeled sub-points + Reflect questions, using
each point's `<!-- anchor: "..." -->` snippet to locate it in the transcript),
and a Key Takeaways table.

Because a sermon-only outline only covers part of the transcript, this script
does NOT backfill leading transcript text into Point 1 the way
`transcript-outline-html` does for the general outline — any pre-sermon
material (worship, announcements, testimonies) is simply excluded, matching
`sermon-outline`'s intent of covering the sermon only.

Usage:
    python merge-html.py <transcript.md> [sermon-outline.md] [--path-only]

If sermon-outline.md is omitted, it's derived from the transcript filename
using the `-claude-transcript.md` -> `-claude-sermon-outline.md` convention.
"""

import re
import sys
from pathlib import Path
from html import escape


def resolve_sermon_outline_path(transcript: Path) -> Path:
    stem = transcript.stem
    if stem.endswith("-claude-transcript"):
        stem = stem[: -len("-claude-transcript")]
        return transcript.parent / f"{stem}-claude-sermon-outline.md"
    return transcript.parent / f"{stem}-sermon-outline.md"


def resolve_output_path(sermon_outline: Path) -> Path:
    stem = re.sub(r"-claude-sermon-outline$", "", sermon_outline.stem)
    return sermon_outline.parent / f"{stem}-claude-sermon.html"


def parse_transcript_body(text: str) -> str:
    lines = text.splitlines()
    body_start = 0
    for i, line in enumerate(lines):
        if line.strip() == "## Transcript":
            body_start = i + 1
            break
    body = "\n".join(lines[body_start:]).strip()
    return re.sub(r"\s+", " ", body).strip()


# --- Minimal markdown -> HTML converter (headers, bold/italic, blockquotes, tables, lists, hr, paragraphs) ---

def inline(text: str) -> str:
    text = escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"\[\[(.+?)\]\]", r"\1", text)
    return text


def convert_markdown(md: str) -> str:
    lines = md.splitlines()
    html, i, para_buf = [], 0, []

    def flush_para():
        if para_buf:
            text = " ".join(para_buf).strip()
            if text:
                html.append(f"<p>{inline(text)}</p>")
            para_buf.clear()

    while i < len(lines):
        stripped = lines[i].strip()

        if stripped == "---":
            flush_para()
            html.append("<hr>")
            i += 1
        elif stripped.startswith("#"):
            flush_para()
            level = min(len(stripped) - len(stripped.lstrip("#")), 6)
            html.append(f"<h{level}>{inline(stripped[level:].strip())}</h{level}>")
            i += 1
        elif stripped.startswith(">"):
            flush_para()
            quote = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip().lstrip(">").strip())
                i += 1
            html.append(f'<div class="callout">{inline(" ".join(quote))}</div>')
        elif stripped.startswith("|"):
            flush_para()
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i].strip())
                i += 1
            html.append(render_table(table_lines))
        elif re.match(r"^[-*]\s+", stripped):
            flush_para()
            items = []
            while i < len(lines) and re.match(r"^[-*]\s+", lines[i].strip()):
                items.append(re.sub(r"^[-*]\s+", "", lines[i].strip()))
                i += 1
            html.append("<ul>" + "".join(f"<li>{inline(it)}</li>" for it in items) + "</ul>")
        elif re.match(r"^\d+\.\s+", stripped):
            flush_para()
            items = []
            while i < len(lines) and re.match(r"^\d+\.\s+", lines[i].strip()):
                items.append(re.sub(r"^\d+\.\s+", "", lines[i].strip()))
                i += 1
            html.append("<ol>" + "".join(f"<li>{inline(it)}</li>" for it in items) + "</ol>")
        elif stripped == "":
            flush_para()
            i += 1
        else:
            para_buf.append(stripped)
            i += 1

    flush_para()
    return "\n".join(html)


def render_table(table_lines) -> str:
    rows = [
        [c.strip() for c in row.strip("|").split("|")]
        for row in table_lines
        if not re.match(r"^\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)*\|?$", row)
    ]
    if not rows:
        return ""
    header, *body = rows
    out = ['<div class="table-wrap"><table>', "<thead><tr>"]
    out += [f"<th>{inline(c)}</th>" for c in header]
    out.append("</tr></thead><tbody>")
    for row in body:
        out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in row) + "</tr>")
    out.append("</tbody></table></div>")
    return "\n".join(out)


# --- Structural sermon-outline parsing ---

ANCHOR_RE = re.compile(r'<!--\s*anchor:\s*"(.*?)"\s*-->')
META_RE = re.compile(r"^\*\*([\w][\w\s/]*):\*\*\s*(.*)$")


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def parse_glossary_rows(glossary_chunk: str):
    """Parses a '## Greek/Hebrew Word Studies' chunk into a list of
    {term, term_display, language, meaning, used_in, slug} dicts.
    `term` is the bare transliteration (e.g. "ergon"), used for matching
    against point text; `term_display` keeps the original markdown (e.g.
    "*ergon* (ἔργον)") for rendering in the table."""
    table_lines = [
        line.strip() for line in glossary_chunk.splitlines() if line.strip().startswith("|")
    ]
    rows = [
        [c.strip() for c in row.strip("|").split("|")]
        for row in table_lines
        if not re.match(r"^\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)*\|?$", row)
    ]
    if len(rows) < 2:
        return []

    glossary = []
    for cols in rows[1:]:
        if len(cols) < 4:
            continue
        word_cell, language, meaning, used_in = cols[0], cols[1], cols[2], cols[3]
        term_match = re.search(r"\*(.+?)\*", word_cell)
        term = term_match.group(1).strip() if term_match else word_cell.strip()
        glossary.append({
            "term": term,
            "term_display": word_cell,
            "language": language,
            "meaning": meaning,
            "used_in": used_in,
            "slug": slugify(term),
        })
    return glossary


def link_glossary_terms(points, glossary):
    """Links each glossary term's first <em> occurrence in the point(s) named in
    its 'Used In' column to that term's glossary row anchor. Best-effort: if a
    point number in 'Used In' doesn't parse or is out of range, that entry is
    skipped rather than erroring."""
    for entry in glossary:
        point_numbers = [int(n) for n in re.findall(r"\d+", entry["used_in"])]
        for n in point_numbers:
            idx = n - 1
            if not (0 <= idx < len(points)):
                continue
            pattern = re.compile(re.escape(f"<em>{escape(entry['term'])}</em>"), re.IGNORECASE)
            linked, count = pattern.subn(
                f'<a href="#glossary-{entry["slug"]}"><em>{escape(entry["term"])}</em></a>',
                points[idx]["html"],
                count=1,
            )
            if count:
                points[idx]["html"] = linked


def parse_sermon_outline(text: str):
    """Returns (meta, overview_html, scripture_html, glossary, points, footer_html).

    meta: dict with title/source/preacher/series/passage.
    glossary: list of {term, term_display, language, meaning, used_in, slug}.
    points: list of {title, anchor, html} in document order.
    """
    lines = text.splitlines()
    meta = {"title": "Untitled", "source": "", "preacher": "", "series": "", "passage": ""}
    frontmatter_end = 0
    for i, line in enumerate(lines):
        if line.startswith("# "):
            title = line[2:].strip()
            meta["title"] = re.sub(r"^Sermon Outline:\s*", "", title)
        m = META_RE.match(line.strip())
        if m:
            key = m.group(1).strip().lower()
            if key in ("source",):
                meta["source"] = m.group(2).strip()
            elif key in ("preacher", "speaker/author", "speaker"):
                meta["preacher"] = m.group(2).strip()
            elif key == "series":
                meta["series"] = m.group(2).strip()
            elif key == "passage":
                meta["passage"] = m.group(2).strip()
        if line.strip() == "---":
            frontmatter_end = i + 1
            break

    body = "\n".join(lines[frontmatter_end:])
    chunks = body.split("\n---\n")

    overview_chunk = chunks[0] if chunks else ""
    scripture_chunk = ""
    glossary_chunk = ""
    points_chunk = ""
    footer_chunks = []

    for chunk in chunks[1:]:
        stripped = chunk.strip()
        if footer_chunks:
            footer_chunks.append(chunk)
        elif stripped.startswith("## Scripture Referenced"):
            scripture_chunk = chunk
        elif stripped.startswith("## Greek/Hebrew Word Studies"):
            glossary_chunk = chunk
        elif stripped.startswith("## Key Takeaways"):
            footer_chunks.append(chunk)
        else:
            points_chunk += ("\n---\n" if points_chunk else "") + chunk

    scripture_chunk = re.sub(r"(?m)^## Scripture Referenced\s*\n", "", scripture_chunk)
    glossary_chunk = re.sub(r"(?m)^## Greek/Hebrew Word Studies\s*\n", "", glossary_chunk)
    footer_chunk = re.sub(r"(?m)^## Key Takeaways\s*\n", "", "\n---\n".join(footer_chunks))

    points = []
    parts = re.split(r"(?m)^## ", points_chunk)
    for part in parts:
        if not part.strip():
            continue
        plines = part.splitlines()
        title = plines[0].strip()
        rest_text = "\n".join(plines[1:])
        anchor_match = ANCHOR_RE.search(rest_text)
        anchor = anchor_match.group(1).strip() if anchor_match else None
        rest_text = ANCHOR_RE.sub("", rest_text)
        points.append({
            "title": title,
            "anchor": anchor,
            "html": convert_markdown(rest_text),
        })

    glossary = parse_glossary_rows(glossary_chunk)
    link_glossary_terms(points, glossary)

    overview_html = convert_markdown(overview_chunk)
    scripture_html = convert_markdown(scripture_chunk)
    footer_html = convert_markdown(footer_chunk)
    return meta, overview_html, scripture_html, glossary, points, footer_html


def slice_transcript(normalized_transcript: str, points):
    """Locate each point's anchor in the transcript. Unlike transcript-outline-html,
    does NOT backfill leading transcript text into point 1 — pre-sermon material
    (worship, announcements, testimonies) is intentionally excluded."""
    positions = []
    for p in points:
        pos = None
        if p["anchor"]:
            anchor_norm = re.sub(r"\s+", " ", p["anchor"]).strip()
            pos = normalized_transcript.find(anchor_norm)
            if pos == -1:
                pos = normalized_transcript.lower().find(anchor_norm.lower())
        positions.append(pos)

    slices = [None] * len(points)
    found = [(i, pos) for i, pos in enumerate(positions) if pos is not None and pos != -1]

    for k, (i, pos) in enumerate(found):
        end = found[k + 1][1] if k + 1 < len(found) else len(normalized_transcript)
        slices[i] = normalized_transcript[pos:end].strip()

    for i, p in enumerate(slices):
        if p is None:
            points[i]["anchor_missing"] = True
            slices[i] = "(Could not locate this point's transcript excerpt automatically.)"

    return slices


def build_blocks(points, transcript_slices) -> str:
    blocks = []
    for idx, (pt, slice_text) in enumerate(zip(points, transcript_slices)):
        transcript_html = "".join(f"<p>{inline(p)}</p>" for p in [slice_text] if p)
        blocks.append(f"""
<section id="point-{idx}">
  <div class="block-header">
    <h2><span class="icon">✝️</span> {inline(pt['title'])}</h2>
    <div class="toggle" role="tablist">
      <button class="toggle-btn active" data-view="summary" role="tab" aria-selected="true">Summary</button>
      <button class="toggle-btn" data-view="transcript" role="tab" aria-selected="false">Transcript</button>
    </div>
  </div>
  <div class="view view-summary active">
    {pt['html']}
  </div>
  <div class="view view-transcript">
    {transcript_html}
  </div>
</section>""")
    return "\n".join(blocks)


def render_glossary_table(glossary) -> str:
    if not glossary:
        return ""
    out = [
        '<div class="table-wrap"><table>',
        "<thead><tr><th>Word</th><th>Language</th><th>Meaning</th><th>Used In</th></tr></thead><tbody>",
    ]
    for row in glossary:
        out.append(
            f'<tr id="glossary-{row["slug"]}">'
            f'<td>{inline(row["term_display"])}</td>'
            f'<td>{inline(row["language"])}</td>'
            f'<td>{inline(row["meaning"])}</td>'
            f'<td>{inline(row["used_in"])}</td>'
            f"</tr>"
        )
    out.append("</tbody></table></div>")
    return "\n".join(out)


def build_nav(points, has_glossary) -> str:
    items = [
        '<li><a href="#overview">Overview</a></li>',
        '<li><a href="#scripture">Scripture Referenced</a></li>',
    ]
    if has_glossary:
        items.append('<li><a href="#glossary">Greek/Hebrew Word Studies</a></li>')
    items += [f'<li><a href="#point-{i}">{inline(p["title"])}</a></li>' for i, p in enumerate(points)]
    items.append('<li><a href="#key-takeaways">Key Takeaways</a></li>')
    return "".join(items)


def build_badges(meta) -> str:
    badges = []
    if meta.get("preacher"):
        badges.append(f'<span class="badge">🎙️ {escape(meta["preacher"])}</span>')
    if meta.get("series"):
        badges.append(f'<span class="badge">📚 {escape(meta["series"])}</span>')
    if meta.get("passage"):
        badges.append(f'<span class="badge">📖 {escape(meta["passage"])}</span>')
    if meta.get("source"):
        badges.append(f'<span class="badge">📺 <a href="{escape(meta["source"])}" target="_blank">Watch on YouTube</a></span>')
    return "".join(badges)


PAGE_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
  :root {{
    --bg: #1B1B2F; --surface: #22223A; --surface2: #2A2A45;
    --accent: #00B4D8; --accent2: #48CAE4; --text: #E0E0E0;
    --muted: #999999; --light: #CCCCCC; --border: #3a3a5c;
    --table-header: #00769E; --table-even: #2A2A45; --table-odd: #22223A;
    --btn-active-fg: #10131c;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html {{ scroll-behavior: smooth; }}
  body {{
    background: var(--bg); color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    font-size: 16px; line-height: 1.7; display: flex; min-height: 100vh;
  }}

  nav {{
    width: 260px; min-width: 260px; background: var(--surface); border-right: 1px solid var(--border);
    padding: 1.2rem 1rem 2rem; position: sticky; top: 0; height: 100vh;
    overflow-y: auto; overflow-x: hidden;
    transition: width 0.22s ease, min-width 0.22s ease, padding 0.22s ease;
  }}
  nav.collapsed {{ width: 48px; min-width: 48px; padding: 1.2rem 0.4rem 2rem; }}
  nav.collapsed .nav-inner {{ opacity: 0; pointer-events: none; }}
  .nav-inner {{ transition: opacity 0.15s ease; }}
  .nav-toggle {{ display: flex; align-items: center; justify-content: flex-end; margin-bottom: 1rem; }}
  .nav-toggle button, .nav-expand {{
    background: var(--surface2); border: 1px solid var(--border); border-radius: 6px;
    color: var(--muted); cursor: pointer; padding: 0.3rem 0.45rem; line-height: 1;
    font-size: 0.9rem; transition: color 0.15s, background 0.15s;
  }}
  .nav-toggle button:hover, .nav-expand:hover {{ color: var(--accent); background: #2e2e4a; }}
  .nav-expand {{ display: none; position: absolute; top: 1.2rem; left: 50%; transform: translateX(-50%); }}
  nav.collapsed .nav-expand {{ display: block; }}
  nav.collapsed .nav-toggle {{ display: none; }}
  nav .logo {{ font-size: 1.05rem; font-weight: 700; color: var(--accent); margin-bottom: 0.3rem; }}
  nav .subtitle {{ font-size: 0.75rem; color: var(--muted); margin-bottom: 1.5rem; word-break: break-word; }}
  nav ul {{ list-style: none; }}
  nav ul li {{ margin: 0.15rem 0; }}
  nav ul li a {{
    display: block; padding: 0.35rem 0.6rem; border-radius: 6px; color: var(--light);
    text-decoration: none; font-size: 0.85rem; transition: background 0.15s, color 0.15s;
    border-left: 3px solid transparent;
  }}
  nav ul li a:hover {{ background: var(--surface2); color: var(--accent2); }}
  nav ul li a.active {{ background: #1e3a42; color: var(--accent); border-left-color: var(--accent); font-weight: 600; }}

  main {{ flex: 1; max-width: 860px; padding: 3rem 3rem 5rem; overflow-x: hidden; }}

  .page-header {{ margin-bottom: 3rem; padding-bottom: 1.5rem; border-bottom: 1px solid var(--border); }}
  .page-header h1 {{ font-size: 2rem; color: var(--accent); font-weight: 800; margin-bottom: 0.5rem; }}
  .page-header .meta {{ display: flex; gap: 0.6rem; flex-wrap: wrap; }}
  .badge {{
    display: inline-flex; align-items: center; gap: 0.3rem; background: var(--surface2);
    border: 1px solid var(--border); border-radius: 20px; padding: 0.2rem 0.7rem;
    font-size: 0.78rem; color: var(--light);
  }}
  .badge a {{ color: var(--accent2); text-decoration: none; }}
  .badge a:hover {{ text-decoration: underline; }}

  section {{ margin-bottom: 3rem; scroll-margin-top: 1rem; }}
  h2 {{
    font-size: 1.4rem; color: var(--accent); font-weight: 700; margin-bottom: 1rem;
    padding-bottom: 0.4rem; border-bottom: 1px solid var(--border);
    display: flex; align-items: center; gap: 0.5rem;
  }}
  h2 .icon {{ font-size: 1.1rem; }}
  p {{ margin-bottom: 0.8rem; color: var(--light); }}
  ul, ol {{ padding-left: 1.4rem; margin-bottom: 0.8rem; color: var(--light); }}
  li {{ margin: 0.3rem 0; }}
  li strong {{ color: var(--accent2); }}

  .table-wrap {{ overflow-x: auto; margin: 0.8rem 0 1rem; border-radius: 8px; border: 1px solid var(--border); }}
  table {{ width: 100%; border-collapse: collapse; }}
  thead th {{ background: var(--table-header); color: #fff; padding: 0.6rem 1rem; text-align: left; font-size: 0.85rem; font-weight: 600; }}
  tbody tr:nth-child(even) td {{ background: var(--table-even); }}
  tbody tr:nth-child(odd) td {{ background: var(--table-odd); }}
  tbody tr:hover td {{ background: #323255; }}
  td {{ padding: 0.5rem 1rem; font-size: 0.875rem; border-top: 1px solid var(--border); color: var(--light); vertical-align: top; }}
  tbody tr:target td {{ background: var(--accent); color: var(--btn-active-fg); }}

  .callout {{
    background: var(--surface2); border-left: 3px solid var(--accent); border-radius: 0 8px 8px 0;
    padding: 0.8rem 1.1rem; margin: 0.8rem 0 1rem; font-size: 0.9rem; color: var(--light); font-style: italic;
  }}

  .block-header {{ display: flex; align-items: center; justify-content: space-between; gap: 1rem; flex-wrap: wrap; margin-bottom: 1rem; }}
  .block-header h2 {{ margin: 0; border-bottom: none; padding-bottom: 0; flex: 1; }}
  .toggle {{ display: inline-flex; background: var(--surface2); border: 1px solid var(--border); border-radius: 999px; padding: 2px; }}
  .toggle-btn {{
    border: none; background: transparent; color: var(--light); font-size: 0.82rem;
    padding: 0.3rem 0.9rem; border-radius: 999px; cursor: pointer;
  }}
  .toggle-btn.active {{ background: var(--accent); color: var(--btn-active-fg); font-weight: 600; }}
  .view {{ display: none; }}
  .view.active {{ display: block; }}

  @media (max-width: 900px) {{
    nav {{ display: none; }}
    main {{ padding: 2rem 1.5rem 4rem; max-width: 100%; }}
  }}
</style>
</head>
<body>

<nav id="sidebar">
  <button class="nav-expand" id="navExpand" title="Expand sidebar">&#x276F;</button>
  <div class="nav-inner">
    <div class="nav-toggle">
      <button id="navCollapse" title="Collapse sidebar">&#x276E;</button>
    </div>
    <div class="logo">Contents</div>
    <div class="subtitle">{title}</div>
    <ul id="navLinks">
      {nav_html}
    </ul>
  </div>
</nav>

<main>
  <div class="page-header">
    <h1>{title}</h1>
    <div class="meta">
      {badges_html}
    </div>
  </div>

  <section id="overview">
    <h2><span class="icon">📝</span> Overview</h2>
    {overview_html}
  </section>

  <section id="scripture">
    <h2><span class="icon">📖</span> Scripture Referenced</h2>
    {scripture_html}
  </section>

  {glossary_section}

  {blocks_html}

  <section id="key-takeaways">
    <h2><span class="icon">✅</span> Key Takeaways</h2>
    {footer_html}
  </section>
</main>

<script>
  const sidebar = document.getElementById('sidebar');
  document.getElementById('navCollapse').addEventListener('click', () => sidebar.classList.add('collapsed'));
  document.getElementById('navExpand').addEventListener('click', () => sidebar.classList.remove('collapsed'));

  const sections = document.querySelectorAll('main section[id]');
  const navLinks = document.querySelectorAll('#navLinks a');

  function setActive(id) {{
    navLinks.forEach(a => {{
      const isActive = a.getAttribute('href') === '#' + id;
      a.classList.toggle('active', isActive);
      if (isActive) a.scrollIntoView({{ block: 'nearest', behavior: 'smooth' }});
    }});
  }}

  const visible = new Map();
  const observer = new IntersectionObserver((entries) => {{
    entries.forEach(e => visible.set(e.target.id, e.isIntersecting));
    for (const section of sections) {{
      if (visible.get(section.id)) {{ setActive(section.id); return; }}
    }}
  }}, {{ rootMargin: '0px 0px -60% 0px', threshold: 0 }});
  sections.forEach(s => observer.observe(s));

  document.querySelectorAll('section').forEach(function (block) {{
    block.querySelectorAll('.toggle-btn').forEach(function (btn) {{
      btn.addEventListener('click', function () {{
        var view = btn.dataset.view;
        block.querySelectorAll('.toggle-btn').forEach(function (b) {{
          b.classList.toggle('active', b === btn);
          b.setAttribute('aria-selected', b === btn ? 'true' : 'false');
        }});
        block.querySelectorAll('.view').forEach(function (v) {{
          v.classList.toggle('active', v.classList.contains('view-' + view));
        }});
      }});
    }});
  }});
</script>
</body>
</html>
"""


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        sys.exit(1)

    transcript_path = Path(args[0]).expanduser().resolve()
    if not transcript_path.exists():
        print(f"Error: transcript file not found: {transcript_path}", file=sys.stderr)
        sys.exit(1)

    sermon_outline_path = (
        Path(args[1]).expanduser().resolve() if len(args) > 1
        else resolve_sermon_outline_path(transcript_path)
    )
    if not sermon_outline_path.exists():
        print(f"Error: sermon outline file not found: {sermon_outline_path}", file=sys.stderr)
        sys.exit(1)

    output_path = resolve_output_path(sermon_outline_path)
    if "--path-only" in sys.argv:
        print(output_path)
        return

    normalized_transcript = parse_transcript_body(transcript_path.read_text())
    meta, overview_html, scripture_html, glossary, points, footer_html = parse_sermon_outline(sermon_outline_path.read_text())

    if not points:
        print("Error: no points found in sermon outline (expected '## N. Title' headings)", file=sys.stderr)
        sys.exit(1)

    missing = [p["title"] for p in points if not p["anchor"]]
    if missing:
        print(f"Warning: {len(missing)} point(s) missing an <!-- anchor: ... --> comment: {missing}", file=sys.stderr)

    transcript_slices = slice_transcript(normalized_transcript, points)
    blocks_html = build_blocks(points, transcript_slices)
    nav_html = build_nav(points, has_glossary=bool(glossary))
    badges_html = build_badges(meta)

    glossary_section = ""
    if glossary:
        glossary_section = (
            '<section id="glossary">\n'
            '<h2><span class="icon">🔤</span> Greek/Hebrew Word Studies</h2>\n'
            f"{render_glossary_table(glossary)}\n"
            "</section>"
        )

    page = PAGE_TEMPLATE.format(
        title=escape(meta["title"]),
        badges_html=badges_html,
        overview_html=overview_html,
        scripture_html=scripture_html,
        glossary_section=glossary_section,
        nav_html=nav_html,
        footer_html=footer_html,
        blocks_html=blocks_html,
    )

    output_path.write_text(page)
    print(f"Saved: {output_path}")
    unresolved = [p["title"] for p in points if p.get("anchor_missing")]
    if unresolved:
        print(f"Warning: {len(unresolved)} point(s) could not be matched to a transcript slice: {unresolved}", file=sys.stderr)


if __name__ == "__main__":
    main()
