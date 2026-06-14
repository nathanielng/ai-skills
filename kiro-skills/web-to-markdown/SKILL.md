---
name: web-to-markdown
description: Convert web pages to clean Markdown. Use when asked to fetch a URL and convert it to markdown, save a web page as markdown, or extract readable content from a website.
---

# Web to Markdown

Fetch a web page or local HTML/MHTML file and convert it to clean Markdown, stripping navigation, scripts, and other noise.

## Prerequisites

```bash
source ~/.venv/bin/activate
python3 -c "import httpx, bs4, markdownify"
```

If missing: `uv pip install httpx beautifulsoup4 markdownify`

## Usage

```bash
source ~/.venv/bin/activate
python3 ~/code/ai-shell/src/web_to_markdown.py <url_or_file>
python3 ~/code/ai-shell/src/web_to_markdown.py <url_or_file> --output file.md
```

### Supported inputs

- **URLs** — fetches the page and converts
- **Local `.html` files** — reads and converts directly
- **Local `.mhtml` / `.mht` files** — extracts HTML from MIME envelope, then converts

## Output Directory

Save all converted pages to `$WEB_PAGES_DIR`. This environment variable must be set (e.g. in `~/.zshrc`). **Fail with an error if it is not set.**

```bash
echo $WEB_PAGES_DIR  # verify it's set
```

## Workflow

1. Activate venv and verify dependencies
2. Run the script with the target URL or local HTML/MHTML file
3. Save output to `$WEB_PAGES_DIR`
4. Present content to user

## Post-processing (automatic)

The script fixes common markdownify artifacts:
- **Broken inline links** — links that end up on their own line are joined back into surrounding text
- **Extra spaces in parentheticals** — `( [link](url) )` → `([link](url))`
- **Excessive newlines** — 3+ consecutive blank lines collapsed to 1
- **Trailing punctuation spacing** — `) ,` → `),`

## Site-specific cleanup

For social media pages (Twitter/X, Reddit, etc.), the automatic conversion may include UI noise (engagement metrics, trending sections, reply boxes). After conversion, manually trim:
- Header/navigation elements
- Engagement counts (likes, retweets, views)
- Sidebar content (trending, suggested follows)
- Footer (terms of service, copyright)

## Limitations

- JavaScript-rendered content won't be captured (static HTML only)
- Some sites may block requests or require authentication
- MHTML files must contain a `text/html` MIME part
