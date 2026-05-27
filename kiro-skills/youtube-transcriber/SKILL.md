---
name: youtube-transcriber
description: Extract transcripts, titles, and author names from YouTube videos. Use when asked to get a transcript, captions, video metadata, summarize a YouTube video's spoken content, or fetch what was said in a video.
---

# YouTube Transcriber

Extract transcripts from YouTube videos using `youtube-transcript-api`. No API key required. Works with auto-generated and manual captions.

## Prerequisites

Before use, verify the dependency is installed:

```bash
pip3 show youtube-transcript-api
```

If not installed:

```bash
uv pip install youtube-transcript-api
```

## Usage

Extract transcript (default):
```bash
python3 ~/code/ai-shell/src/extractors/youtube_transcriber.py <youtube_url_or_video_id>
```

Extract metadata:
```bash
# Video title
python3 ~/code/ai-shell/src/extractors/youtube_transcriber.py <video_id> --title

# Author/channel name
python3 ~/code/ai-shell/src/extractors/youtube_transcriber.py <video_id> --author

# Filename slug (title-videoid)
python3 ~/code/ai-shell/src/extractors/youtube_transcriber.py <video_id> --slug
```

Accepts any standard YouTube URL format:
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/embed/VIDEO_ID`
- Or just the video ID directly

## Examples

### Extract transcript
```bash
# Full URL
python3 ~/code/ai-shell/src/extractors/youtube_transcriber.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Short URL
python3 ~/code/ai-shell/src/extractors/youtube_transcriber.py "https://youtu.be/dQw4w9WgXcQ"

# Video ID only
python3 ~/code/ai-shell/src/extractors/youtube_transcriber.py dQw4w9WgXcQ
```

### Extract metadata
```bash
# Get the video title
python3 ~/code/ai-shell/src/extractors/youtube_transcriber.py dQw4w9WgXcQ --title

# Get the channel/author name
python3 ~/code/ai-shell/src/extractors/youtube_transcriber.py dQw4w9WgXcQ --author

# Get filename slug
python3 ~/code/ai-shell/src/extractors/youtube_transcriber.py dQw4w9WgXcQ --slug
```

## Output Directory

Save all transcripts to `$YOUTUBE_TRANSCRIPTIONS_DIR`. This environment variable must be set (e.g. in `~/.zshrc`). **Fail with an error if it is not set.**

```bash
echo $YOUTUBE_TRANSCRIPTIONS_DIR  # verify it's set
```

Filename format: `<slugified-title>-<VIDEO_ID>-transcript.txt`

Use `--slug` to generate a suggested filename:

```bash
# Get the slug for naming
SLUG=$(python3 ~/code/ai-shell/src/extractors/youtube_transcriber.py dQw4w9WgXcQ --slug)
# Transcript will be saved to: $YOUTUBE_TRANSCRIPTIONS_DIR/$SLUG-transcript.txt
```

## Workflow

1. Check `youtube-transcript-api` is installed; install if missing
2. Run the transcriber with the provided URL or video ID
3. Save output to `$YOUTUBE_TRANSCRIPTIONS_DIR`
4. Present the transcript text to the user
5. If no transcript is available (disabled captions, private video), inform the user

## Limitations

- Only works on videos with captions enabled (auto-generated or manual)
- Default language is English; other languages may be available depending on the video
- Private or age-restricted videos may not be accessible
