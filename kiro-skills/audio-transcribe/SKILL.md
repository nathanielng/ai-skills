---
name: audio-transcribe
description: Transcribe audio files (mp3, wav, m4a, etc.) to text on-device using Apple Silicon GPU via Metal. Use when asked to transcribe audio, convert speech to text, generate subtitles, or extract text from audio/video files.
---

# Audio Transcribe — On-Device Speech-to-Text (Apple Silicon)

Transcribe audio files locally on Mac using Metal GPU acceleration. No cloud APIs or keys required.

## Two Backends

| | mlx-whisper (default) | mlx-audio (Qwen3-ASR) |
|---|---|---|
| Model | whisper-large-v3-turbo (809M) | Qwen3-ASR-0.6B-8bit |
| Memory | ~6GB | Lower (quantized) |
| Languages | 99+ | 52 + 22 Chinese dialects |
| English | Very good | Competitive |
| CJK | Good | **Better** |
| Timestamps | Segment-level | Word-level (with aligner) |
| Maturity | **Mature** | Recent |

**Use mlx-whisper** for English and general multilingual work.
**Use mlx-audio** for Mandarin/Cantonese/CJK or when word-level timestamps are needed.

## Prerequisites

```bash
source ~/.venv/bin/activate
```

Install one or both:

```bash
uv pip install mlx-whisper    # default
uv pip install mlx-audio      # for Qwen3-ASR / CJK
```

Models download automatically on first use (~1.6GB for whisper-large-v3-turbo).

## Usage — mlx-whisper (default)

### CLI

```bash
mlx_whisper audio.mp3 --model mlx-community/whisper-large-v3-turbo --language en
```

### Python

```python
import mlx_whisper

result = mlx_whisper.transcribe(
    "audio.mp3",
    path_or_hf_repo="mlx-community/whisper-large-v3-turbo",
    language="en"
)
print(result["text"])
```

## Usage — mlx-audio (Qwen3-ASR)

### CLI

```bash
uv run mlx_audio.stt.generate \
  --model mlx-community/Qwen3-ASR-0.6B-8bit \
  --audio audio.wav \
  --language English
```

### Python

```python
from mlx_audio.stt import load

model = load("mlx-community/Qwen3-ASR-0.6B-8bit")
result = model.generate("audio.wav", language="English")
print(result.text)
```

## Output Directory

Save all transcripts to `$AUDIO_TRANSCRIPTIONS_DIR`. This environment variable must be set (e.g. in `~/.zshrc`). **Fail with an error if it is not set.**

```bash
echo $AUDIO_TRANSCRIPTIONS_DIR  # verify it's set
```

Filename format: `<original_filename>-transcript.txt`

## Workflow

1. Check backend is installed; install if missing
2. Choose backend based on language (CJK → mlx-audio, otherwise → mlx-whisper)
3. Run transcription
4. Save output to `$AUDIO_TRANSCRIPTIONS_DIR`
5. Present transcript to user

## Notes

- First run downloads the model to `~/.cache/huggingface`
- Quantized variant available: `LibraxisAI/whisper-large-v3-turbo-mlx-q8` (lower memory)
- Word-level alignment: use `Qwen3-ForcedAligner-0.6B-8bit` with mlx-audio
- Supported formats: mp3, wav, m4a, flac, ogg, webm
