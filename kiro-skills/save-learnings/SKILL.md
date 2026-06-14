---
name: save-learnings
description: Extract and save important learnings from conversations to your Obsidian vault. Use when the user wants to save something they learned, store knowledge for later, or manage their learnings collection.
---

# Save Learnings — Obsidian Knowledge Capture

Extract and save important learnings to your Obsidian vault, organized by category with YAML frontmatter.

## Prerequisites

```bash
source ~/.venv/bin/activate
export OBSIDIAN_PATH="$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianVault"
```

## Usage

```bash
python3 ~/code/ai-skills/claude-skills/save-learnings/save-learnings.py              # Interactive
python3 ~/code/ai-skills/claude-skills/save-learnings/save-learnings.py --list       # List all
python3 ~/code/ai-skills/claude-skills/save-learnings/save-learnings.py --list --json
python3 ~/code/ai-skills/claude-skills/save-learnings/save-learnings.py --json       # Batch (stdin)
python3 ~/code/ai-skills/claude-skills/save-learnings/save-learnings.py --update FILE
```

## Batch Save (non-interactive)

```bash
echo '[
  {"title":"Topic","content":"What I learned","category":"aws","tags":["tag1"]}
]' | python3 ~/code/ai-skills/claude-skills/save-learnings/save-learnings.py --json
```

## List with Filters

```bash
python3 ~/code/ai-skills/claude-skills/save-learnings/save-learnings.py --list --category aws
python3 ~/code/ai-skills/claude-skills/save-learnings/save-learnings.py --list --since 2026-05-01
```

## Storage

All learnings saved to `$OBSIDIAN_PATH/ai-learnings/` organized by category:

```
ai-learnings/
├── aws/
│   └── 2026-05-24-bedrock-inference.md
├── ai/
│   └── 2026-05-22-rag-architecture.md
└── 2026-05-20-general-learning.md
```

## Integration

After saving, query learnings with the `pageindex` skill.
