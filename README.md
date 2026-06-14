# ai-skills

A collection of skills for AI coding agents — Claude Code and Kiro. Skills are organised by agent since each uses a different format.

## Structure

```
ai-skills/
├── claude-skills/        # Claude Code skills (Claude Code SKILL.md format)
│   ├── aws-spend/        # AWS cost report with caching and HTML dashboard
│   ├── bedrock-troubleshoot/  # Diagnose AWS Bedrock issues
│   ├── commit-check/     # Scan staged changes for secrets, PII, hardcoded paths
│   ├── create-guide/     # Generate structured guides from conversation context
│   ├── discussion-to-plan/   # Convert discussion threads into structured plans
│   ├── pageindex/        # Query Obsidian vault via PageIndex (vectorless RAG)
│   ├── save-learnings/   # Save learnings from conversations to Obsidian vault
│   └── upload-lambda-layer/  # Publish zip files as AWS Lambda layers
│
├── kiro-skills/          # Kiro skills (Kiro SKILL.md format with YAML frontmatter)
│   ├── audio-transcribe/ # On-device speech-to-text via Apple Silicon Metal
│   ├── bedrock-troubleshoot/  # Diagnose AWS Bedrock issues
│   ├── pageindex/        # Query Obsidian vault via PageIndex
│   ├── pdf-to-markdown/  # Convert PDFs to Markdown via OpenDataLoader
│   ├── save-learnings/   # Save learnings to Obsidian vault
│   ├── web-to-markdown/  # Fetch web pages and convert to Markdown
│   └── youtube-transcriber/  # Extract transcripts from YouTube videos
│
└── shared/               # Agent-agnostic scripts and utilities
    ├── gws/              # Google Workspace CLI wrappers (rate limiting, audit log)
    └── tests/            # Test suite for shared utilities
```

## Skill formats

The two agents use different SKILL.md schemas — do not mix them.

**Claude Code** (`claude-skills/`): Markdown heading format
```markdown
# Skill Name

Description of what the skill does.

## Invocation
/skill-name

## Implementation
...
```

**Kiro** (`kiro-skills/`): YAML frontmatter format
```markdown
---
name: skill-name
description: One-line description used for skill discovery and triggering.
---

# Skill Name
...
```

## Adding a new skill

1. Determine which agent the skill is for
2. Create a directory under `claude-skills/` or `kiro-skills/`
3. Add a `SKILL.md` in the correct format for that agent
4. Add any supporting scripts alongside the SKILL.md
5. Add sensitive or generated files (credentials, cache, outputs) to a `.gitignore` in the skill directory

## Notes

- Some skills exist in both `claude-skills/` and `kiro-skills/` — the implementations are independent since the agents invoke skills differently
- `shared/gws/` contains Google Workspace CLI wrappers with rate limiting and audit logging; see `claude-skills/README.md` for usage
- Skills that reference external scripts (e.g. `~/code/ai-shell/`) depend on those repos being present separately
