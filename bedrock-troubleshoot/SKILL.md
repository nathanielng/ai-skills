# bedrock-troubleshoot

Diagnose and fix common AWS Bedrock issues for both Claude/Anthropic and Mantle/OpenAI-compatible paths.

## Usage

```bash
python /path/to/diagnose.py              # Interactive mode
python /path/to/diagnose.py --claude     # Diagnose Claude path only
python /path/to/diagnose.py --mantle     # Diagnose Mantle path only
python /path/to/diagnose.py --help       # Show help
```

## What it does

Runs automated diagnostics:
- ✓ Verifies AWS credentials are configured
- ✓ Checks Bedrock access in correct region
- ✓ Lists available models (Claude or Qwen/OSS)
- ✓ Identifies common configuration errors
- ✓ Suggests specific fixes

## Two Paths

### Claude Path (boto3)
```bash
python /path/to/diagnose.py --claude
```
Checks for:
- Correct model ID format (`us.anthropic.claude-sonnet-4-6`)
- Region (`us-east-1`)
- API version (`bedrock-2023-05-31`)
- IAM permissions

### Mantle Path (OpenAI-compatible)
```bash
python /path/to/diagnose.py --mantle
```
Checks for:
- Region support (us-west-2, etc.)
- Qwen/OSS model availability
- Bearer token generation
- OpenAI SDK compatibility

## Reference Docs

- **Implementation Guide**: See `ai-learnings/aws/Bedrock-Implementation-Guide.md` (queryable via `/pageindex`)
- **Claude-specific notes**: See `ai-learnings/aws/Claude-Bedrock-Inference-Profile-Format.md`

## Common Issues

| Error | Solution |
|-------|----------|
| `ValidationException: Could not validate input` | Model ID format wrong; use `us.anthropic.claude-sonnet-4-6` |
| `AccessDeniedException: not authorized` | IAM permissions missing `bedrock:InvokeModel` |
| `Unknown service: bedrock-runtime` | API version wrong; must be `bedrock-2023-05-31` |
| `401 Unauthorized` (Mantle) | Bearer token expired; regenerate with `aws-bedrock-token-generator` |
| `Region not supported` (Mantle) | Try us-west-2; not all regions have Mantle |
