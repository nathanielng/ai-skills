#!/usr/bin/env python3
"""
YouTube Transcriber Skill - Claude Code integration

Extracts transcripts from YouTube videos without requiring an API key.
Supports full URLs and video IDs, with auto-generated and manual captions.
"""

import sys
import os
import logging
from pathlib import Path

# Add the ai-shell source directory to path
if "AI_SHELL_SRC" not in os.environ:
    print("Error: AI_SHELL_SRC environment variable must be set", file=sys.stderr)
    sys.exit(1)
ai_shell_src = Path(os.environ["AI_SHELL_SRC"])
sys.path.insert(0, str(ai_shell_src))

from extractors.youtube_transcriber import get_transcript, extract_video_id, get_title, slugify

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


def main():
    if len(sys.argv) < 2:
        print("Usage: youtube-transcriber <youtube_url_or_video_id>")
        print("\nExamples:")
        print("  youtube-transcriber 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'")
        print("  youtube-transcriber 'dQw4w9WgXcQ'")
        sys.exit(1)

    arg = sys.argv[1].strip("'\"")

    # Extract video ID from URL or use directly if already an ID
    video_id = extract_video_id(arg) if "://" in arg or "/" in arg else arg

    if not video_id:
        print(f"Error: Could not extract video ID from: {arg}", file=sys.stderr)
        sys.exit(1)

    # Fetch transcript
    transcript = get_transcript(video_id)

    if transcript:
        # Get video title for friendlier filename
        title = get_title(video_id)
        title_slug = slugify(title) if title else "untitled"
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        markdown = (
            f"# {title or 'Untitled'}\n\n"
            f"- **URL:** {video_url}\n"
            f"- **Video ID:** {video_id}\n\n"
            f"## Transcript\n\n"
            f"{transcript}\n"
        )

        # Save to output directory (set via env var)
        if "YOUTUBE_TRANSCRIPTIONS_DIR" not in os.environ:
            print("Error: YOUTUBE_TRANSCRIPTIONS_DIR environment variable must be set", file=sys.stderr)
            sys.exit(1)
        save_dir = Path(os.environ["YOUTUBE_TRANSCRIPTIONS_DIR"])
        save_dir.mkdir(parents=True, exist_ok=True)

        # Save with {VIDEO_ID}-{title_slug}-claude-transcript.md naming convention
        output_file = save_dir / f"{video_id}-{title_slug}-claude-transcript.md"
        output_file.write_text(markdown)

        print(markdown)
        print(f"\n✓ Saved to: {output_file}", file=sys.stderr)
        sys.exit(0)
    else:
        print(f"Error: No transcript available for video: {video_id}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
