---
name: pdf-to-markdown
description: Convert PDF files to Markdown using OpenDataLoader PDF. Use when asked to extract text from a PDF, convert PDF to markdown, parse PDF tables, or prepare PDF content for RAG/LLM ingestion.
---

# PDF to Markdown

Convert PDF files to clean Markdown using [OpenDataLoader PDF](https://github.com/opendataloader-project/opendataloader-pdf). Deterministic local mode (no GPU, no API key). Hybrid mode available for complex tables, scanned PDFs, and formulas.

## Prerequisites

Requires Java 11+ and Python 3.10+.

```bash
java -version  # must be 11+
source ~/.venv/bin/activate
uv pip install -U opendataloader-pdf
```

For hybrid mode (complex tables, OCR, formulas):

```bash
uv pip install -U "opendataloader-pdf[hybrid]"
```

## Usage

### CLI

```bash
source ~/.venv/bin/activate
opendataloader-pdf input.pdf                          # markdown to stdout dir
opendataloader-pdf input.pdf --output-dir output/     # save to directory
opendataloader-pdf file1.pdf file2.pdf folder/        # batch
```

### Python

```python
import opendataloader_pdf

opendataloader_pdf.convert(
    input_path=["input.pdf"],
    output_dir="output/",
    format="markdown"
)
```

## Output Directory

Save converted markdown to `$PDF_PAGES_DIR`. This environment variable must be set (e.g. in `~/.zshrc`). **Fail with an error if it is not set.**

```bash
echo $PDF_PAGES_DIR  # verify it's set
```

## Modes

| Document type | Mode | Command |
|---|---|---|
| Standard digital PDF | Fast (default) | `opendataloader-pdf input.pdf` |
| Complex/borderless tables | Hybrid | Start server: `opendataloader-pdf-hybrid --port 5002`, then: `opendataloader-pdf --hybrid docling-fast input.pdf` |
| Scanned/image PDF | Hybrid + OCR | Start server: `opendataloader-pdf-hybrid --port 5002 --force-ocr` |
| Math formulas | Hybrid + formula | Start server: `opendataloader-pdf-hybrid --enrich-formula`, client: `--hybrid-mode full` |

## Output Formats

- `markdown` — clean text for LLM/RAG (default)
- `json` — structured with bounding boxes
- `markdown,json` — both

## Workflow

1. Verify Java 11+ and `opendataloader-pdf` installed; install if missing
2. Run conversion on the PDF file(s)
3. Save output to `$PDF_PAGES_DIR`
4. Present content to user

## Limitations

- Requires Java 11+ runtime
- Each `convert()` call spawns a JVM process — batch multiple files in one call for efficiency
- Hybrid mode requires starting a separate server process
- No GPU required
