# save-learnings

Extract and save important learnings from conversations to your Obsidian vault.

## Setup

Set your Obsidian vault path before running:

```bash
export OBSIDIAN_PATH="$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianVault"
```

(Adjust path for your system if different)

## Usage

```bash
python /path/to/save-learnings.py              # Interactive mode
python /path/to/save-learnings.py --list       # List all learnings
python /path/to/save-learnings.py --list --json # List as JSON
python /path/to/save-learnings.py --json       # Batch mode (stdin)
python /path/to/save-learnings.py --update FILE # Update existing learning
python /path/to/save-learnings.py --help       # Show help
```

## How it works

1. **Interactive mode** — Prompts you to enter a title, markdown content, optional category, and tags
2. **Batch mode** — Reads JSON array from stdin, saves multiple learnings at once
3. **List mode** — Shows all saved learnings organized by category with previews
4. **Update mode** — Revises existing learnings and tracks modification timestamps
5. **Storage** — All learnings saved to `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianVault/ai-learnings/`

## Examples

**Interactive save:**
```bash
python /path/to/save-learnings.py
# Prompts for: Title, Content, Category (optional), Tags (optional)
```

**Batch save from JSON:**
```bash
echo '[
  {"title":"Bedrock Inference Profiles","content":"Must use us.anthropic.claude-sonnet-4-6 format","category":"aws","tags":["bedrock","inference"]},
  {"title":"RAG Architecture","content":"Vector embeddings via sentence-transformers, FAISS for retrieval","category":"ai"}
]' | python /path/to/save-learnings.py --json
```

**List with filters:**
```bash
python /path/to/save-learnings.py --list                        # All learnings
python /path/to/save-learnings.py --list --category aws        # AWS category only
python /path/to/save-learnings.py --list --since 2026-05-01    # Since a date
python /path/to/save-learnings.py --list --json                # Output as JSON
```

**Update a learning:**
```bash
python /path/to/save-learnings.py --update ai-learnings/aws/2026-05-24-bedrock.md
# Prompts to edit title, content, category, or tags
```

## File organization

Each learning is saved as a timestamped markdown file with YAML frontmatter:

```
ai-learnings/
├── aws/
│   ├── 2026-05-24-bedrock-inference.md
│   └── 2026-05-23-iam-user-setup.md
├── ai/
│   ├── 2026-05-22-rag-architecture.md
│   └── 2026-05-21-vector-embeddings.md
└── 2026-05-20-general-learning.md (no category)
```

**Frontmatter format:**
```yaml
---
title: My Learning
date: 2026-05-24
time: 15:30:45
category: aws
tags: ["bedrock", "inference"]
modified: 2026-05-24  # Only if updated
---
```

## Integration with /pageindex

After saving learnings, query them with `/pageindex`:

```bash
/pageindex "What did I learn about Bedrock?"
/pageindex "Show me my RAG learnings"
```

The PageIndex skill will search across all saved learnings in your vault and synthesize answers from your saved knowledge.
