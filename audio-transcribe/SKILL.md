# audio-transcribe

Transcribe audio files to text on-device using Apple Silicon GPU via Metal. No cloud APIs or keys required.

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

## Setup

Activate your Python environment:

```bash
source ~/.venv/bin/activate
```

Install one or both backends:

```bash
uv pip install mlx-whisper    # default
uv pip install mlx-audio      # for Qwen3-ASR / CJK
```

Models download automatically on first use (~1.6GB for whisper-large-v3-turbo).

## Usage — CLI

```bash
# mlx-whisper (default, English)
python audio-transcriber.py audio.mp3

# mlx-audio (CJK languages)
python audio-transcriber.py audio.mp3 --backend qwen3

# With language hint
python audio-transcriber.py audio.mp3 --language en

# Custom output directory
python audio-transcriber.py audio.mp3 -o /path/to/output
```

## Usage — Module

```python
from audio_transcriber import transcribe

# Basic transcription
transcript = transcribe("audio.mp3")
print(transcript)

# With options
transcript = transcribe(
    "audio.mp3",
    backend="mlx-whisper",
    language="en"
)
```

## Output

Transcripts are saved to `$AUDIO_TRANSCRIPTIONS_DIR` (if set) with filename format: `<original_filename>-transcript.txt`

If the environment variable is not set, use the `-o/--output` flag to specify an output directory.

## Supported Formats

mp3, wav, m4a, flac, ogg, webm

## Notes

- First run downloads the model to `~/.cache/huggingface`
- Quantized variant available: `LibraxisAI/whisper-large-v3-turbo-mlx-q8` (lower memory)
- Word-level alignment: use `Qwen3-ForcedAligner-0.6B-8bit` with mlx-audio backend
