# YouTube Transcriber Skill

Extract transcripts and subtitles from YouTube videos without requiring an API key.

## Features
- Supports full YouTube URLs and video IDs
- Works with auto-generated and manual captions
- Multiple language support
- Simple CLI and Python API

## Invocation

### Via CLI
```bash
$PYTHON "$CLAUDE_SKILLS_DIR/youtube-transcriber/youtube-transcriber.py" "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
$PYTHON "$CLAUDE_SKILLS_DIR/youtube-transcriber/youtube-transcriber.py" "dQw4w9WgXcQ"
```

Environment variables (set these in `~/.zshrc` or equivalent):
- `$PYTHON` — Path to Python interpreter
- `$CLAUDE_SKILLS_DIR` — Path to skills directory
- `$AI_SHELL_SRC` — Path to ai-shell source directory
- `$YOUTUBE_TRANSCRIPTIONS_DIR` — Output directory for transcripts

### Via Python API
```python
from youtube_transcriber import get_transcript, get_title, slugify, extract_video_id

# Using video ID
transcript = get_transcript("dQw4w9WgXcQ")

# Using URL
video_id = extract_video_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
transcript = get_transcript(video_id)

# With language preferences
transcript = get_transcript("dQw4w9WgXcQ", languages=['en', 'es'])

# Get video title
title = get_title("dQw4w9WgXcQ")
title_slug = slugify(title)  # Safe for filenames
```

## Implementation

Script location: `$CLAUDE_SKILLS_DIR/youtube-transcriber/youtube-transcriber.py`

Dependencies:
- `youtube-transcript-api` (install via `uv pip install youtube-transcript-api`)
- Requires `$AI_SHELL_SRC` environment variable to be set

## Output

Transcripts are automatically saved as Markdown to:
```
$YOUTUBE_TRANSCRIPTIONS_DIR/{VIDEO_ID}-{title_slug}-claude-transcript.md
```

Each file includes the video title and URL as a header, followed by the transcript:
```markdown
# {Video Title}

- **URL:** https://www.youtube.com/watch?v={VIDEO_ID}
- **Video ID:** {VIDEO_ID}

## Transcript

{transcript text}
```

Example filename: `lXUZvyajciY-decade-of-agents-karpathy-claude-transcript.md`

The markdown is also printed to stdout. Naming convention groups all artifacts from the same video together by video ID (e.g., `lXUZvyajciY-claude-outline.md`, `lXUZvyajciY-decade-of-agents-karpathy-claude-transcript.md`).

## Supported URL Formats

- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://youtube.com/embed/VIDEO_ID`
- `https://youtube.com/v/VIDEO_ID`
- Raw video ID
