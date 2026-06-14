#!/usr/bin/env python3
"""
Save Learnings - Extract and save important learnings from conversations to Obsidian vault.
Usage: python save-learnings.py [options]
"""
import sys
import os
import json
from pathlib import Path
from datetime import datetime
import re

obsidian_path = os.environ.get("OBSIDIAN_PATH")
if not obsidian_path:
    raise ValueError(
        "OBSIDIAN_PATH environment variable not set.\n"
        "Set it to your Obsidian vault path, e.g.:\n"
        "export OBSIDIAN_PATH=\"$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianVault\"\n"
        "or equivalent for your system."
    )

vault_path = Path(obsidian_path).expanduser()
if not vault_path.exists():
    raise ValueError(f"Obsidian vault path does not exist: {vault_path}")

learnings_dir = vault_path / "ai-learnings"
learnings_dir.mkdir(exist_ok=True)

def sanitize_filename(text: str) -> str:
    filename = re.sub(r'[^a-zA-Z0-9\s-]', '', text)
    filename = re.sub(r'\s+', '-', filename).lower()
    return filename[:50]

def extract_frontmatter(filepath: Path) -> dict:
    content = filepath.read_text(encoding='utf-8')
    if not content.startswith('---'):
        return {}

    lines = content.split('\n')
    end_idx = next((i for i in range(1, len(lines)) if lines[i] == '---'), -1)
    if end_idx == -1:
        return {}

    fm = {}
    for line in lines[1:end_idx]:
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            if key == 'tags':
                try:
                    fm[key] = json.loads(value)
                except:
                    fm[key] = []
            else:
                fm[key] = value
    return fm

def get_learning_preview(filepath: Path) -> str:
    content = filepath.read_text(encoding='utf-8')
    if not content.startswith('---'):
        return content[:77] + '...' if len(content) > 80 else content

    lines = content.split('\n')
    end_idx = next((i for i in range(1, len(lines)) if lines[i] == '---'), -1)
    if end_idx == -1:
        return content[:77] + '...' if len(content) > 80 else content

    preview = '\n'.join(lines[end_idx+2:end_idx+3]).strip()
    return (preview[:77] + '...') if len(preview) > 80 else preview

def save_learning(title: str, content: str, category: str = None, tags: list = None) -> dict:
    timestamp = datetime.now()
    date_str = timestamp.strftime("%Y-%m-%d")
    time_str = timestamp.strftime("%H:%M:%S")

    if category:
        save_dir = learnings_dir / category
        save_dir.mkdir(exist_ok=True)
    else:
        save_dir = learnings_dir

    filename_base = sanitize_filename(title)
    filename = f"{date_str}-{filename_base}.md"
    filepath = save_dir / filename

    frontmatter = f"""---
title: {title}
date: {date_str}
time: {time_str}
category: {category or 'general'}
tags: {json.dumps(tags or [])}
---

"""

    markdown = frontmatter + content
    filepath.write_text(markdown, encoding='utf-8')

    return {
        "success": True,
        "file": str(filepath.relative_to(vault_path)),
        "path": str(filepath),
        "category": category or "general",
        "timestamp": f"{date_str} {time_str}"
    }

def update_learning(filepath: Path, content: str = None, title: str = None, category: str = None, tags: list = None) -> dict:
    if not filepath.exists():
        return {"success": False, "error": f"File not found: {filepath}"}

    fm = extract_frontmatter(filepath)
    title = title or fm.get('title', 'Untitled')
    category = category or fm.get('category', 'general')
    tags = tags if tags is not None else json.loads(fm.get('tags', '[]')) if 'tags' in fm else []

    timestamp = datetime.now()
    date_str = timestamp.strftime("%Y-%m-%d")
    time_str = timestamp.strftime("%H:%M:%S")
    original_date = fm.get('date', date_str)

    frontmatter = f"""---
title: {title}
date: {original_date}
time: {time_str}
modified: {date_str}
category: {category}
tags: {json.dumps(tags)}
---

"""

    markdown = frontmatter + (content or "")
    filepath.write_text(markdown, encoding='utf-8')

    return {
        "success": True,
        "file": str(filepath.relative_to(vault_path)),
        "path": str(filepath),
        "timestamp": f"{date_str} {time_str}"
    }

def save_learnings_batch(learnings: list) -> list:
    results = []
    for learning in learnings:
        try:
            result = save_learning(
                title=learning.get("title", "Untitled"),
                content=learning.get("content", ""),
                category=learning.get("category"),
                tags=learning.get("tags")
            )
            results.append(result)
        except Exception as e:
            results.append({
                "success": False,
                "title": learning.get("title", "Unknown"),
                "error": str(e)
            })

    return results

def list_learnings(category_filter: str = None, since: str = None, output_json: bool = False):
    since_date = None
    if since:
        try:
            since_date = datetime.strptime(since, "%Y-%m-%d").date()
        except ValueError:
            print("❌ Invalid date format. Use YYYY-MM-DD")
            return

    learnings = []

    for category_dir in sorted(learnings_dir.iterdir()):
        if category_dir.is_dir():
            if category_filter and category_dir.name != category_filter:
                continue

            for f in sorted(category_dir.glob("*.md")):
                fm = extract_frontmatter(f)
                try:
                    file_date = datetime.strptime(fm.get('date', ''), "%Y-%m-%d").date()
                    if since_date and file_date < since_date:
                        continue
                except:
                    pass

                tags = fm.get('tags', [])
                if isinstance(tags, str):
                    tags = json.loads(tags)
                learnings.append({
                    "file": str(f.relative_to(vault_path)),
                    "title": fm.get('title', f.stem),
                    "category": fm.get('category', 'general'),
                    "date": fm.get('date', ''),
                    "time": fm.get('time', ''),
                    "tags": tags,
                    "preview": get_learning_preview(f)
                })

    for f in sorted(learnings_dir.glob("*.md")):
        if category_filter and category_filter != 'general':
            continue

        fm = extract_frontmatter(f)
        try:
            file_date = datetime.strptime(fm.get('date', ''), "%Y-%m-%d").date()
            if since_date and file_date < since_date:
                continue
        except:
            pass

        tags = fm.get('tags', [])
        if isinstance(tags, str):
            tags = json.loads(tags)
        learnings.append({
            "file": str(f.relative_to(vault_path)),
            "title": fm.get('title', f.stem),
            "category": fm.get('category', 'general'),
            "date": fm.get('date', ''),
            "time": fm.get('time', ''),
            "tags": tags,
            "preview": get_learning_preview(f)
        })

    if output_json:
        print(json.dumps(learnings, indent=2))
    else:
        if not learnings:
            print("No learnings found.")
            return

        print("📚 Saved Learnings\n")
        print("=" * 80)

        current_category = None
        for learning in learnings:
            if learning['category'] != current_category:
                current_category = learning['category']
                print(f"\n📁 {current_category}")

            print(f"\n   📝 {learning['title']}")
            print(f"      📅 {learning['date']} {learning['time']}")
            if learning['tags']:
                print(f"      🏷️  {', '.join(learning['tags'])}")
            if learning['preview']:
                print(f"      > {learning['preview']}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("""
Usage: python save-learnings.py [OPTIONS]

Modes:
  (no args)              Interactive mode - prompts for title, content, category, tags
  --json                 Batch mode - read JSON array from stdin
  --list                 List all saved learnings with previews
  --list --json          List as JSON
  --list --category TAG  Filter list by category
  --list --since DATE    Filter by date (YYYY-MM-DD)
  --update FILE          Update an existing learning file
  --help                 Show this help message

Examples:
  python save-learnings.py
  python save-learnings.py --list --category bedrock
  python save-learnings.py --list --since 2026-05-01
  echo '[{"title":"My Learning","content":"Details","category":"aws"}]' | python save-learnings.py --json
""")

    elif len(sys.argv) > 1 and sys.argv[1] == "--list":
        category_filter = None
        since_filter = None
        output_json = False

        i = 2
        while i < len(sys.argv):
            if sys.argv[i] == "--category" and i + 1 < len(sys.argv):
                category_filter = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--since" and i + 1 < len(sys.argv):
                since_filter = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--json":
                output_json = True
                i += 1
            else:
                i += 1

        list_learnings(category_filter, since_filter, output_json)

    elif len(sys.argv) > 1 and sys.argv[1] == "--json":
        try:
            data = json.loads(sys.stdin.read())
            results = save_learnings_batch(data)

            print(json.dumps(results, indent=2))

            print("\n✅ Learnings Saved")
            print("=" * 60)
            for r in results:
                if r.get("success"):
                    print(f"✓ {r['file']}")
                else:
                    print(f"✗ {r['title']}: {r.get('error', 'Unknown error')}")

        except json.JSONDecodeError:
            print("❌ Invalid JSON input")
            sys.exit(1)

    elif len(sys.argv) > 1 and sys.argv[1] == "--update":
        if len(sys.argv) < 3:
            print("❌ --update requires a file path")
            sys.exit(1)

        update_filepath = Path(sys.argv[2])
        if not update_filepath.exists():
            update_filepath = learnings_dir / sys.argv[2]

        if not update_filepath.exists():
            print(f"❌ File not found: {sys.argv[2]}")
            sys.exit(1)

        print("📝 Update Learning")
        print("=" * 60)

        current_fm = extract_frontmatter(update_filepath)

        new_title = input(f"Title (current: '{current_fm.get('title')}'): ").strip() or None
        print("\nContent (leave empty to keep current, paste markdown, Ctrl+D to finish):")
        lines = []
        try:
            while True:
                line = input()
                lines.append(line)
        except EOFError:
            pass

        new_content = "\n".join(lines) if lines else None
        new_category = input(f"Category (current: '{current_fm.get('category')}'): ").strip() or None

        current_tags = json.loads(current_fm.get('tags', '[]'))
        tags_input = input(f"Tags (current: {current_tags}, comma-separated): ").strip()
        new_tags = [t.strip() for t in tags_input.split(",") if t.strip()] if tags_input else None

        result = update_learning(update_filepath, new_content, new_title, new_category, new_tags)

        if result.get("success"):
            print("\n✅ Learning Updated!")
            print(f"File: {result['file']}")
            print(f"Timestamp: {result['timestamp']}")
        else:
            print(f"\n❌ Error: {result.get('error')}")
            sys.exit(1)

    else:
        print("📝 Save a Learning to Your Vault")
        print("=" * 60)

        title = input("\nTitle: ").strip()
        if not title:
            print("❌ Title is required")
            sys.exit(1)

        print("\nContent (paste markdown, Ctrl+D to finish):")
        lines = []
        try:
            while True:
                line = input()
                lines.append(line)
        except EOFError:
            pass

        content = "\n".join(lines)
        category = input("\nCategory (optional, e.g. 'bedrock', 'rag'): ").strip() or None
        tags_input = input("Tags (comma-separated, optional): ").strip()
        tags = [t.strip() for t in tags_input.split(",") if t.strip()] if tags_input else None

        result = save_learning(title, content, category, tags)

        print("\n✅ Learning Saved!")
        print(f"File: {result['file']}")
        print(f"Path: {result['path']}")
        print(f"Category: {result['category']}")
        print(f"Timestamp: {result['timestamp']}")
