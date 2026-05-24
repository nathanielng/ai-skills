#!/usr/bin/env python3
"""
Create-Guide Skill: Generate comprehensive guides from conversation context.

Extracts learnings, workflows, pitfalls, and troubleshooting from conversations
and structures them into a professional guide with:
- Quick start
- Step-by-step workflow
- Troubleshooting
- Pitfalls to avoid
- Verification checklists

Usage:
    python3 create-guide.py --topic "HyperFrames Setup" --output guide.md
    python3 create-guide.py --help
"""

import json
import sys
import argparse
from datetime import datetime
from pathlib import Path


class GuideGenerator:
    """Generate comprehensive guides from conversation context."""

    def __init__(self, topic, description=""):
        self.topic = topic
        self.description = description
        self.sections = {
            "quick_start": [],
            "workflow": [],
            "troubleshooting": [],
            "pitfalls": [],
            "verification": [],
        }

    def add_quick_start(self, steps, prerequisites="", time_estimate=""):
        """Add quick start section."""
        self.sections["quick_start"] = {
            "time": time_estimate,
            "prerequisites": prerequisites,
            "steps": steps,
        }

    def add_workflow_step(self, step_number, name, description, checklist, verification):
        """Add a workflow step."""
        self.sections["workflow"].append({
            "number": step_number,
            "name": name,
            "description": description,
            "checklist": checklist,
            "verification": verification,
        })

    def add_troubleshooting(self, problem, cause, solution):
        """Add troubleshooting entry."""
        self.sections["troubleshooting"].append({
            "problem": problem,
            "cause": cause,
            "solution": solution,
        })

    def add_pitfall(self, title, description, why, fix):
        """Add a pitfall to avoid."""
        self.sections["pitfalls"].append({
            "title": title,
            "description": description,
            "why": why,
            "fix": fix,
        })

    def add_verification_item(self, phase, items):
        """Add verification checklist for a phase."""
        self.sections["verification"].append({
            "phase": phase,
            "items": items,
        })

    def generate_markdown(self):
        """Generate markdown guide."""
        md = []

        # Header
        md.append(f"# {self.topic}")
        if self.description:
            md.append(self.description)
        md.append("")
        md.append("---")
        md.append("")

        # Quick Start
        if self.sections["quick_start"]:
            qs = self.sections["quick_start"]
            md.append("## Quick Start")
            if qs.get("time"):
                md.append(f"**Time:** {qs['time']}")
            if qs.get("prerequisites"):
                md.append("### Prerequisites")
                md.append(qs["prerequisites"])
                md.append("")
            for step in qs.get("steps", []):
                md.append(f"- {step}")
            md.append("")
            md.append("✅ **Verification:** All steps complete, no errors")
            md.append("")
            md.append("---")
            md.append("")

        # Workflow
        if self.sections["workflow"]:
            md.append("## Step-by-Step Workflow")
            md.append("")
            for step in self.sections["workflow"]:
                md.append(f"### {step['number']}. {step['name']}")
                md.append("")
                md.append(f"**What you're doing:** {step['description']}")
                md.append("")
                if step.get("checklist"):
                    md.append("**Critical checklist:**")
                    for item in step["checklist"]:
                        md.append(f"- [ ] {item}")
                    md.append("")
                if step.get("verification"):
                    md.append("✅ **Verification:**")
                    for item in step["verification"]:
                        md.append(f"- {item}")
                    md.append("")
                md.append("---")
                md.append("")

        # Troubleshooting
        if self.sections["troubleshooting"]:
            md.append("## Troubleshooting Guide")
            md.append("")
            md.append("| Problem | Cause | Solution |")
            md.append("|---------|-------|----------|")
            for ts in self.sections["troubleshooting"]:
                problem = ts["problem"].replace("|", "\\|")
                cause = ts["cause"].replace("|", "\\|")
                solution = ts["solution"].replace("|", "\\|")
                md.append(f"| {problem} | {cause} | {solution} |")
            md.append("")
            md.append("---")
            md.append("")

        # Pitfalls
        if self.sections["pitfalls"]:
            md.append("## Pitfalls to Avoid")
            md.append("")
            for i, pitfall in enumerate(self.sections["pitfalls"], 1):
                md.append(f"### {i}. {pitfall['title']}")
                md.append(f"**Pitfall:** {pitfall['description']}")
                md.append(f"**Why:** {pitfall['why']}")
                md.append(f"**Fix:** {pitfall['fix']}")
                md.append("")

            md.append("---")
            md.append("")

        # Verification Checklists
        if self.sections["verification"]:
            md.append("## Verification Checklist")
            md.append("")
            md.append("Use this at key steps to confirm everything is working:")
            md.append("")
            for verify in self.sections["verification"]:
                md.append(f"### {verify['phase']}")
                for item in verify["items"]:
                    md.append(f"- [ ] {item}")
                md.append("")

        # Footer
        md.append("---")
        md.append(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d')}")
        md.append("**Version:** 1.0")

        return "\n".join(md)

    def save(self, output_path):
        """Save guide to markdown file."""
        markdown = self.generate_markdown()
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        Path(output_path).write_text(markdown)
        print(f"✅ Guide saved to {output_path}")


def create_example_hyperframes_guide():
    """Create example HyperFrames guide (for demonstration)."""
    guide = GuideGenerator(
        topic="HyperFrames Setup Guide",
        description="**Complete workflow for creating, animating, adding audio, and rendering Christian animations**"
    )

    # Quick Start
    guide.add_quick_start(
        steps=[
            "`npx hyperframes init my-animation` — Scaffold project",
            "`npx hyperframes lint` — Check for errors",
            "`npx hyperframes preview --port 3005` — Preview in browser",
            "`npx hyperframes render --quality high` — Create final MP4",
        ],
        prerequisites="Node.js 22+, ffmpeg (for audio), screen (for managing servers)",
        time_estimate="5 minutes"
    )

    # Workflow
    guide.add_workflow_step(
        1, "Create Composition",
        "Build visual design, typography, colors, and GSAP animations",
        [
            "All scenes have entrance animations",
            "No exit animations except final scene",
            "`data-composition-id` on root div",
            "Timeline registered in `window.__timelines`",
        ],
        [
            "`npx hyperframes lint` returns no errors",
            "`npx hyperframes inspect` shows no overflow",
            "Preview loads and animations play smoothly",
        ]
    )

    guide.add_workflow_step(
        2, "Find Royalty-Free Music",
        "Source CC0 music matching animation mood and duration",
        [
            "Search by mood (uplifting, contemplative, peaceful)",
            "Filter by duration (45s, 65s, etc.)",
            "Verify license is CC0 or Creative Commons",
            "Download as MP3",
        ],
        [
            "File downloads without errors",
            "File size reasonable (3-5MB for 45-65s)",
            "Audio plays locally",
        ]
    )

    guide.add_workflow_step(
        3, "Validate Audio Quality",
        "Confirm downloaded file is real audio, not corrupted or silent",
        [
            "Check file size (3-5MB, not 175KB)",
            "Check volume with ffmpeg volumedetect",
            "Listen to file locally",
        ],
        [
            "File size: 3-5MB",
            "Max volume: >= -0.9dB (not -91dB)",
            "Audio plays clearly when opened",
        ]
    )

    guide.add_workflow_step(
        4, "Integrate Music",
        "Add audio file to HyperFrames composition",
        [
            "File copied to `music/` subdirectory",
            "HTML `src` path matches file location",
            "`data-duration` matches animation length",
            "`data-volume` between 0.7-0.8",
        ],
        [
            "File exists at `music/filename.mp3`",
            "Path in HTML matches actual location",
            "Audio plays in preview (not silent)",
        ]
    )

    guide.add_workflow_step(
        5, "Test in Preview",
        "Verify audio plays correctly before rendering",
        [
            "Start preview server",
            "Play composition",
            "Check audio syncs with animation",
            "Check audio volume is appropriate",
        ],
        [
            "Audio plays when you hit play",
            "You can hear the music clearly",
            "Audio stops at end",
            "No console errors",
        ]
    )

    guide.add_workflow_step(
        6, "Render Final Video",
        "Create final MP4 with audio embedded",
        [
            "Run `npx hyperframes render --quality high`",
            "Verify MP4 file created",
            "Verify audio in MP4 with ffprobe",
        ],
        [
            "Render completes without errors",
            "MP4 file created",
            "MP4 has audio track (ffprobe shows codec=aac)",
            "Audio in sync with animation",
        ]
    )

    # Troubleshooting
    guide.add_troubleshooting(
        "No sound in preview",
        "Silent audio file (-91dB) or wrong path",
        "Validate with ffmpeg, redownload, check HTML path"
    )

    guide.add_troubleshooting(
        "Downloaded file is HTML",
        "Website returned error page",
        "Try different source or direct download link"
    )

    guide.add_troubleshooting(
        "Audio cuts off early",
        "Duration mismatch between animation and audio",
        "Update `data-duration` to match animation length"
    )

    guide.add_troubleshooting(
        "Render fails",
        "Out of memory or font loading timeout",
        "Close other apps, use `--workers 2`, run `npx hyperframes doctor`"
    )

    # Pitfalls
    guide.add_pitfall(
        "Silent Placeholder Audio",
        "Downloaded audio plays in browser but rendering creates silent MP4",
        "Audio file corrupted or was silent placeholder (ffmpeg -t 45)",
        "Always validate with ffmpeg volumedetect BEFORE integrating. Reject if max < -60dB."
    )

    guide.add_pitfall(
        "Path Mismatches",
        "HTML says `src=\"music/song.mp3\"` but file is somewhere else",
        "Easy to forget exact filename or copy to wrong location",
        "Triple-check: verify file path, file location, use relative paths"
    )

    guide.add_pitfall(
        "Duration Mismatches",
        "Animation is 45 seconds but `data-duration=\"65\"`",
        "Easy to use wrong value or forget to update after timing changes",
        "When speeding up animation by 1.5x, divide duration by 1.5"
    )

    guide.add_pitfall(
        "Background Processes Die",
        "Started preview with `&` and lost process when terminal closed",
        "Background processes die with shell, no way to manage",
        "Use screen sessions: `screen -S name -d -m bash -c \"command\"`"
    )

    # Verification
    guide.add_verification_item(
        "Before Creating Animations",
        [
            "Node.js 22+ installed: `node --version`",
            "ffmpeg installed: `ffmpeg -version`",
            "Can run HyperFrames: `npx hyperframes --version`",
        ]
    )

    guide.add_verification_item(
        "After Downloading Music",
        [
            "File size reasonable (3-5MB for 45-65s)",
            "Max volume >= -0.9dB (check with ffmpeg)",
            "Can hear audio: `open file.mp3`",
            "License is CC0 or Creative Commons",
        ]
    )

    guide.add_verification_item(
        "After Rendering",
        [
            "MP4 file created: `ls -lh *.mp4`",
            "File has audio: `ffprobe -select_streams a:0 ...`",
            "Audio plays: `open file.mp4`",
            "Duration is correct",
            "Audio is in sync with animation",
        ]
    )

    return guide


def main():
    parser = argparse.ArgumentParser(
        description="Generate comprehensive guides from conversation context"
    )
    parser.add_argument(
        "--example",
        action="store_true",
        help="Generate example HyperFrames guide"
    )
    parser.add_argument(
        "--output",
        default="GUIDE.md",
        help="Output markdown file (default: GUIDE.md)"
    )
    parser.add_argument(
        "--topic",
        default="Comprehensive Guide",
        help="Guide topic/title"
    )

    args = parser.parse_args()

    if args.example:
        guide = create_example_hyperframes_guide()
        guide.save(args.output)
        print(f"\n📚 Example guide created: {args.output}")
        print("\nTo create custom guides:")
        print("  1. Create a Python script using GuideGenerator class")
        print("  2. Add sections: quick_start, workflow, troubleshooting, pitfalls, verification")
        print("  3. Call guide.save(output_path)")


if __name__ == "__main__":
    main()
