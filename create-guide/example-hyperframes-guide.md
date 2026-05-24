# HyperFrames Setup Guide
**Complete workflow for creating, animating, adding audio, and rendering Christian animations**

---

## Quick Start
**Time:** 5 minutes
### Prerequisites
Node.js 22+, ffmpeg (for audio), screen (for managing servers)

- `npx hyperframes init my-animation` — Scaffold project
- `npx hyperframes lint` — Check for errors
- `npx hyperframes preview --port 3005` — Preview in browser
- `npx hyperframes render --quality high` — Create final MP4

✅ **Verification:** All steps complete, no errors

---

## Step-by-Step Workflow

### 1. Create Composition

**What you're doing:** Build visual design, typography, colors, and GSAP animations

**Critical checklist:**
- [ ] All scenes have entrance animations
- [ ] No exit animations except final scene
- [ ] `data-composition-id` on root div
- [ ] Timeline registered in `window.__timelines`

✅ **Verification:**
- `npx hyperframes lint` returns no errors
- `npx hyperframes inspect` shows no overflow
- Preview loads and animations play smoothly

---

### 2. Find Royalty-Free Music

**What you're doing:** Source CC0 music matching animation mood and duration

**Critical checklist:**
- [ ] Search by mood (uplifting, contemplative, peaceful)
- [ ] Filter by duration (45s, 65s, etc.)
- [ ] Verify license is CC0 or Creative Commons
- [ ] Download as MP3

✅ **Verification:**
- File downloads without errors
- File size reasonable (3-5MB for 45-65s)
- Audio plays locally

---

### 3. Validate Audio Quality

**What you're doing:** Confirm downloaded file is real audio, not corrupted or silent

**Critical checklist:**
- [ ] Check file size (3-5MB, not 175KB)
- [ ] Check volume with ffmpeg volumedetect
- [ ] Listen to file locally

✅ **Verification:**
- File size: 3-5MB
- Max volume: >= -0.9dB (not -91dB)
- Audio plays clearly when opened

---

### 4. Integrate Music

**What you're doing:** Add audio file to HyperFrames composition

**Critical checklist:**
- [ ] File copied to `music/` subdirectory
- [ ] HTML `src` path matches file location
- [ ] `data-duration` matches animation length
- [ ] `data-volume` between 0.7-0.8

✅ **Verification:**
- File exists at `music/filename.mp3`
- Path in HTML matches actual location
- Audio plays in preview (not silent)

---

### 5. Test in Preview

**What you're doing:** Verify audio plays correctly before rendering

**Critical checklist:**
- [ ] Start preview server
- [ ] Play composition
- [ ] Check audio syncs with animation
- [ ] Check audio volume is appropriate

✅ **Verification:**
- Audio plays when you hit play
- You can hear the music clearly
- Audio stops at end
- No console errors

---

### 6. Render Final Video

**What you're doing:** Create final MP4 with audio embedded

**Critical checklist:**
- [ ] Run `npx hyperframes render --quality high`
- [ ] Verify MP4 file created
- [ ] Verify audio in MP4 with ffprobe

✅ **Verification:**
- Render completes without errors
- MP4 file created
- MP4 has audio track (ffprobe shows codec=aac)
- Audio in sync with animation

---

## Troubleshooting Guide

| Problem | Cause | Solution |
|---------|-------|----------|
| No sound in preview | Silent audio file (-91dB) or wrong path | Validate with ffmpeg, redownload, check HTML path |
| Downloaded file is HTML | Website returned error page | Try different source or direct download link |
| Audio cuts off early | Duration mismatch between animation and audio | Update `data-duration` to match animation length |
| Render fails | Out of memory or font loading timeout | Close other apps, use `--workers 2`, run `npx hyperframes doctor` |

---

## Pitfalls to Avoid

### 1. Silent Placeholder Audio
**Pitfall:** Downloaded audio plays in browser but rendering creates silent MP4
**Why:** Audio file corrupted or was silent placeholder (ffmpeg -t 45)
**Fix:** Always validate with ffmpeg volumedetect BEFORE integrating. Reject if max < -60dB.

### 2. Path Mismatches
**Pitfall:** HTML says `src="music/song.mp3"` but file is somewhere else
**Why:** Easy to forget exact filename or copy to wrong location
**Fix:** Triple-check: verify file path, file location, use relative paths

### 3. Duration Mismatches
**Pitfall:** Animation is 45 seconds but `data-duration="65"`
**Why:** Easy to use wrong value or forget to update after timing changes
**Fix:** When speeding up animation by 1.5x, divide duration by 1.5

### 4. Background Processes Die
**Pitfall:** Started preview with `&` and lost process when terminal closed
**Why:** Background processes die with shell, no way to manage
**Fix:** Use screen sessions: `screen -S name -d -m bash -c "command"`

---

## Verification Checklist

Use this at key steps to confirm everything is working:

### Before Creating Animations
- [ ] Node.js 22+ installed: `node --version`
- [ ] ffmpeg installed: `ffmpeg -version`
- [ ] Can run HyperFrames: `npx hyperframes --version`

### After Downloading Music
- [ ] File size reasonable (3-5MB for 45-65s)
- [ ] Max volume >= -0.9dB (check with ffmpeg)
- [ ] Can hear audio: `open file.mp3`
- [ ] License is CC0 or Creative Commons

### After Rendering
- [ ] MP4 file created: `ls -lh *.mp4`
- [ ] File has audio: `ffprobe -select_streams a:0 ...`
- [ ] Audio plays: `open file.mp4`
- [ ] Duration is correct
- [ ] Audio is in sync with animation

---
**Last Updated:** 2026-05-24
**Version:** 1.0