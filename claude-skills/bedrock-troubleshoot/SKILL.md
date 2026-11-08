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
| `ValueError: Cannot specify both api_key and AWS credentials` (Claude SDK / `AnthropicBedrock`) | See **AWS_BEARER_TOKEN_BEDROCK conflicts with SigV4 creds** below |
| `403 ... "Authentication failed: Please make sure your API Key is valid"` even though `aws sts get-caller-identity` works | Same cause — see below |

## AWS_BEARER_TOKEN_BEDROCK conflicts with SigV4 creds

If `AWS_BEARER_TOKEN_BEDROCK` is set in your shell environment (Bedrock's newer
API-key auth mode), it silently takes priority in some clients and causes hard
failures in others — it does **not** gracefully fall back to IAM/SigV4:

- The `anthropic` SDK's `AnthropicBedrock` client reads `AWS_BEARER_TOKEN_BEDROCK`
  from the environment unconditionally as its default `api_key`, *before* looking
  at any `aws_profile`/`aws_access_key` you pass in. If the token is present
  **and** SigV4 credentials are also configured/passed, the SDK raises
  `ValueError: Cannot specify both api_key and AWS credentials` rather than
  picking one.
- If the token itself is stale/invalid and nothing else is passed, you instead
  get a `403` whose message ("Please make sure your API Key is valid") looks
  like an IAM problem but isn't — `aws sts get-caller-identity` will succeed
  fine because that's a completely different credential path.

**Diagnose**: `echo "${AWS_BEARER_TOKEN_BEDROCK:+set}"` — if that prints `set`,
the env var is present and is the likely culprit whenever a Bedrock call fails
despite valid AWS credentials.

**Fix**, in order of preference:
1. If you don't need the bearer-token/API-key auth path, unset it for the
   session: `unset AWS_BEARER_TOKEN_BEDROCK` (or remove it from `~/.zshrc`/
   `~/.zshenv` if it's set globally there).
2. In code that should always use IAM/SigV4 (e.g. a long-running app, not an
   interactive shell), explicitly clear it before constructing the client:
   `os.environ.pop("AWS_BEARER_TOKEN_BEDROCK", None)` — passing `aws_profile`
   alone is **not** sufficient, since the SDK reads the env var first and
   raises on the conflict rather than letting your explicit arg win.
3. If you specifically want to use the bearer-token/API-key path instead,
   don't pass any of `aws_profile`/`aws_access_key`/`aws_secret_key`/
   `aws_session_token` — those are what trigger the conflict check.

This bit an AI-coding-assistant session that had `AWS_BEARER_TOKEN_BEDROCK`
set from unrelated prior work while also having valid IAM creds configured —
the model ID looked wrong at first (400 on a bad ID after clearing the var),
but the *actual* blocker until then was this env var conflict producing a
403 that read like an auth/IAM issue.
