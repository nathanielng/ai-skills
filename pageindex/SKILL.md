# pageindex

Query your Obsidian vault using PageIndex (vectorless, reasoning-based RAG) with Claude via AWS Bedrock.

## Setup

Set your Obsidian vault path before running:

```bash
export OBSIDIAN_PATH="$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianVault"
```

(Adjust path for your system if different)

## Usage

```bash
python /path/to/obsidian-pageindex.py "QUESTION"
python /path/to/obsidian-pageindex.py               # Interactive mode
```

## How it works

1. **Semantic search** across 574 indexed chunks from your Obsidian vault
2. **PageIndex** vectorless retrieval (reasoning-based, not similarity-based)
3. **Claude Sonnet 4.6** via AWS Bedrock generates answers from context
4. **Fallback mode** if Bedrock fails (shows context for manual reasoning)

## Examples

```bash
python /path/to/obsidian-pageindex.py "What are my main work projects?"
python /path/to/obsidian-pageindex.py "Tell me about my spiritual interests"
python /path/to/obsidian-pageindex.py               # Interactive mode
```

## Configuration

- **Python script**: `~/code/ai-skills/pageindex/obsidian-pageindex.py`
- **Vault path**: Set via `OBSIDIAN_PATH` environment variable (no hardcoded paths)
- **Vector store**: `$OBSIDIAN_PATH/rag-vectorstore`
- **Bedrock config**:
  - IAM user: `vault-bedrock` (configured in AWS credentials)
  - Region: `us-east-1` (global endpoint)
  - Model ID: `us.anthropic.claude-sonnet-4-6` (inference profile)
  - API version: `bedrock-2023-05-31`

## Based on

[PageIndex](https://github.com/VectifyAI/PageIndex) — Document Index for Vectorless, Reasoning-based RAG by VectifyAI
