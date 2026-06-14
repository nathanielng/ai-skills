# GWS CLI Wrappers for Claude

Safe Python wrappers around the Google Workspace CLI (`gws`) with rate limiting, confirmation prompts, and audit logging.

## Features

- **Rate Limiting**: 30 calls/minute (shared across Gmail and Calendar)
- **Confirmation Prompts**: Preview dry-run output before executing destructive operations
- **Audit Logging**: Every call logged to `logs/gws.log` with timestamp, arguments, and exit status
- **Non-interactive Mode**: Use `--force` to skip confirmations, `--dry-run-only` for read-only preview

## Requirements

- `gws` CLI installed and authenticated
- Python 3.7+

## Installation

1. Clone this repo:
```bash
git clone https://github.com/nathanielng/ai-skills.git
cd ai-skills/shared/gws
```

2. Make scripts executable:
```bash
chmod +x gws_*.py
```

3. (Optional) Add to PATH for easier access:
```bash
export PATH="$PATH:$(pwd)"
```

## Usage

### Gmail Operations

Read-only (no confirmation needed):
```bash
python3 gws_gmail.py users getProfile
python3 gws_gmail.py users.messages list
```

Destructive operations (with confirmation):
```bash
python3 gws_gmail.py +send --to user@example.com --subject "Test" --body "Hello"
# Shows dry-run output, prompts: Execute for real? [y/N]
```

Skip confirmation:
```bash
python3 gws_gmail.py +send --to user@example.com --subject "Test" --body "Hello" --force
```

### Calendar Operations

```bash
python3 gws_calendar.py calendarList list
python3 gws_calendar.py +insert --summary "Meeting" --startTime "2026-05-15T10:00:00"
```

### Flags

- `--force` — Skip confirmation prompt (rate limit and logging still apply)
- `--dry-run-only` — Run with `--dry-run` and exit without prompting

## Destructive Operations (Require Confirmation)

**Gmail:**
- `+send`, `+reply`, `+reply-all`, `+forward`
- `messages.delete`, `messages.trash`, `messages.modify`
- `drafts.delete`, `labels.delete`
- `threads.delete`, `threads.modify`, `threads.trash`

**Calendar:**
- `+insert`, `events.insert`, `events.delete`, `events.update`, `events.patch`, `events.quickAdd`, `events.move`
- `calendars.insert`, `calendars.delete`, `calendars.clear`, `calendars.update`, `calendars.patch`
- `acl` and `calendarList` modifications

## Audit Log

All calls are logged to `logs/gws.log` in JSON format:

```json
{"ts": "2026-05-10T21:33:58.680334", "service": "calendar", "args": ["calendarList", "list"], "status": "ok", "note": "exit code 0"}
```

## Rate Limiting

The rate limiter persists to `~/.cache/gws-wrapper/rate.json`. The 30 calls/minute window is shared across both Gmail and Calendar wrappers.

```bash
# This will fail on the 31st call within a minute
for i in {1..31}; do python3 gws_gmail.py users getProfile; done
# Error: Rate limit exceeded: 30 calls/min. Reset in ~60s.
```

## Integration with Claude

Update your Claude skill files to use these wrappers:

```markdown
## Safe Wrapper

Use the Python wrapper for all operations:

```bash
python3 ~/path/to/scripts/gws_gmail.py <resource> <method> [flags]
```

The wrapper adds rate limiting, confirmation prompts, dry-run preview, and audit logging.
```

## Testing

Run the test suite:

```bash
python3 -m pytest ../tests/ -v
```

Or run with coverage:

```bash
python3 -m pytest ../tests/ --cov=. --cov-report=html
```

## License

MIT — see LICENSE file for details.
