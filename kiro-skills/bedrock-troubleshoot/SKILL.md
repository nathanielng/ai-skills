---
name: bedrock-troubleshoot
description: Diagnose and fix AWS Bedrock issues for Claude/Anthropic and Mantle/OpenAI-compatible paths. Use when encountering Bedrock errors, model access issues, authentication failures, or needing to verify Bedrock configuration.
---

# Bedrock Troubleshoot — AWS Bedrock Diagnostics

Automated diagnostics for AWS Bedrock covering both Claude (boto3) and Mantle (OpenAI-compatible) paths.

## Prerequisites

```bash
source ~/.venv/bin/activate
python3 -c "import boto3"
```

If missing: `uv pip install boto3`

## Usage

```bash
python3 ~/code/ai-skills/claude-skills/bedrock-troubleshoot/diagnose.py              # Interactive
python3 ~/code/ai-skills/claude-skills/bedrock-troubleshoot/diagnose.py --claude     # Claude path only
python3 ~/code/ai-skills/claude-skills/bedrock-troubleshoot/diagnose.py --mantle     # Mantle path only
```

## What It Checks

- AWS credentials configured correctly
- Bedrock access in correct region
- Available models (Claude or Qwen/OSS)
- Common configuration errors with specific fixes

## Two Paths

### Claude (boto3)
- Model ID: `us.anthropic.claude-sonnet-4-6`
- Region: `us-east-1`
- API version: `bedrock-2023-05-31` <!-- gitleaks:allow -->
- IAM permissions: `bedrock:InvokeModel`

### Mantle (OpenAI-compatible)
- Region: `us-west-2`
- Qwen/OSS model availability
- Bearer token generation
- OpenAI SDK compatibility

## Common Issues

| Error | Fix |
|-------|-----|
| `Could not validate input` | Use `us.anthropic.claude-sonnet-4-6` format |
| `AccessDeniedException` | Add `bedrock:InvokeModel` to IAM |
| `Unknown service: bedrock-runtime` | Use API version `bedrock-2023-05-31` |
| `401 Unauthorized` (Mantle) | Regenerate bearer token |
| `Region not supported` (Mantle) | Use `us-west-2` |

## Reference Docs

Query via `pageindex` skill:
- `ai-learnings/aws/Bedrock-Implementation-Guide.md`
- `ai-learnings/aws/Claude-Bedrock-Inference-Profile-Format.md`
