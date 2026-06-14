---
name: pageindex
description: Query your Obsidian vault using PageIndex (vectorless, reasoning-based RAG) with Claude via AWS Bedrock. Use when asked to search notes, find information in the vault, recall learnings, or answer questions from personal knowledge base.
---

# PageIndex — Obsidian Vault RAG

Query your Obsidian vault using PageIndex (vectorless, reasoning-based RAG) with Claude via AWS Bedrock.

## Prerequisites

```bash
source ~/.venv/bin/activate
python3 -c "import boto3, sentence_transformers, faiss"
```

If missing: `uv pip install boto3 sentence-transformers faiss-cpu`

## Usage

```bash
source ~/.venv/bin/activate
export OBSIDIAN_PATH="$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianVault"
python3 ~/code/ai-skills/claude-skills/pageindex/obsidian-pageindex.py "QUESTION"
python3 ~/code/ai-skills/claude-skills/pageindex/obsidian-pageindex.py   # Interactive mode
```

## Configuration

- **Script**: `~/code/ai-skills/claude-skills/pageindex/obsidian-pageindex.py`
- **Vault path**: Set via `OBSIDIAN_PATH` environment variable
- **Vector store**: `$OBSIDIAN_PATH/rag-vectorstore`
- **Bedrock**: region `us-east-1`, model `us.anthropic.claude-sonnet-4-6`

## Examples

```bash
python3 ~/code/ai-skills/claude-skills/pageindex/obsidian-pageindex.py "What are my main work projects?"
python3 ~/code/ai-skills/claude-skills/pageindex/obsidian-pageindex.py "What did I learn about Bedrock?"
```

## Based on

[PageIndex](https://github.com/VectifyAI/PageIndex) — Vectorless, Reasoning-based RAG by VectifyAI
