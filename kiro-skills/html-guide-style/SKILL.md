---
name: html-guide-style
description: A reusable dark-themed, single-page HTML style for reference guides, cheat sheets, and docs, with a collapsible sidebar (active-section highlighting), badges, callouts, styled code blocks, tables, quick-reference grid, and link cards. Use when asked to turn notes or reference material into a polished standalone HTML guide/cheat sheet.
---

# html-guide-style

A reusable dark-themed, single-page HTML style for reference guides, cheat sheets, and docs: a collapsible sidebar with active-section highlighting, badges, callouts, styled code blocks, tables, a quick-reference grid, and a links grid. Self-contained (inline CSS/JS, no external requests, no build step).

## When to Use

Invoke this whenever asked to turn notes, a README, a cheat sheet, or reference material into a single polished HTML page — anything in the shape of "getting started guide," "cheat sheet," or "reference doc." Not intended for long-form prose (articles, transcripts) — it's built for scannable, section-and-table-heavy technical content.

## How to Use

1. Read `template.html` in this skill's directory — it's a complete, working page with placeholder markers (`{{PAGE_TITLE}}`, `{{NAV_LINKS}}`, `{{SECTIONS}}`, etc.) and inline comments showing every available component.
2. Copy it and fill in the placeholders:
   - `{{PAGE_TITLE}}` — `<title>` tag text.
   - `{{LOGO_LABEL}}` — short label/icon in the sidebar header (can be plain text or include an inline `<svg>`).
   - `{{SUBTITLE}}` — small text under the logo (e.g. "Getting Started · macOS").
   - `{{PAGE_H1}}` — the big heading in the main content header.
   - `{{BADGES}}` — zero or more `<span class="badge">...</span>` pills (platform, date, version, source link, etc.).
   - `{{NAV_LINKS}}` — one `<li><a href="#section-id">Title</a></li>` per top-level `<section id="section-id">`, in document order. Group with `<li class="section-label">Group Name</li>` if useful.
   - `{{SECTIONS}}` — the actual content, one `<section id="...">` per nav link, built from the components below.
3. Every top-level `<section>` needs a matching `id` and nav link — the sidebar's active-section highlighting (via `IntersectionObserver`) depends on this pairing.
4. Save as a single `.html` file. No external dependencies, safe to open directly from disk or host anywhere.

## Components

| Component | Markup |
|---|---|
| Section heading | `<h2><span class="icon">🖥️</span> Title</h2>` — the emoji icon is optional but matches the style |
| Sub-heading | `<h3>...</h3>` |
| Callout (neutral) | `<div class="callout">...</div>` |
| Callout (tip) | `<div class="callout tip"><strong>Tip:</strong> ...</div>` |
| Callout (warning) | `<div class="callout warn"><strong>Note:</strong> ...</div>` |
| Code block | `<pre><code><span class="comment"># comment</span>\ncode line</code><span class="lang-label">bash</span></pre>` |
| Inline code | `` <code>...</code> `` |
| Keyboard key | `<kbd>Ctrl</kbd>+<kbd>p</kbd>` |
| Table | `<div class="table-wrap"><table><thead>...</thead><tbody>...</tbody></table></div>` — always wrap tables in `.table-wrap` for horizontal scroll on overflow |
| Quick-reference grid | `<div class="quick-ref"><div class="qr-item"><span class="want">...</span><span class="keys">...</span></div></div>` — for "if you want X, press/run Y" cheat-sheet rows |
| Link cards grid | `<div class="links-grid"><a class="link-card" href="..." target="_blank"><span class="link-icon">📖</span> Label</a></div>` |

## Design Notes

- Fixed dark palette (not `prefers-color-scheme`-aware) — the whole point is a consistent, deliberate dark aesthetic, not a light/dark toggle. If the user wants a light variant, treat it as a distinct ask rather than adding a media query here.
- Sidebar collapses to a 48px icon rail (not fully hidden) via a `.collapsed` class toggled by two buttons (`navCollapse` / `navExpand`); on screens ≤900px the sidebar hides entirely and content goes full-width.
- Accent color (`--accent: #00B4D8`) and the rest of the palette are CSS custom properties in `:root` — safe to retint for a different project by changing the variable values only, everything else derives from them.
- Keep section count reasonable (roughly 6–15) — the sidebar nav and active-highlighting are built for a single-page doc with a clear table of contents, not a deeply nested wiki.
