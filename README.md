# doc-chunker

A lightweight Python utility for splitting documents into text chunks for RAG. It reads the text from the file and cuts it into pieces of a size you choose, with overlap. It runs locally and needs no model, no server and no credentials.

doc-chunker currently supports:

- PDF
- DOCX
- PPTX
- TXT and MD

Scanned PDFs and images have no text layer. Use doc-extract for those.

## Prerequisites

- Python 3.9 or newer

Everything runs on your machine. Your documents never leave it.

## Installation

```bash
pip install doc-chunker
```

Alternatively, you can install it from the source:

```bash
pip install .
```

## Usage

### Command-Line

Print the chunks in the terminal:

```bash
doc-chunker manual.pdf
```

Write the result to a file:

```bash
doc-chunker manual.pdf -o manual.jsonl
```

Several files, with your own sizes. With several inputs, `-o` is a folder and each input gets `<full name>.jsonl`:

```bash
doc-chunker a.pdf b.docx -o out/ --chunk-size 800 --overlap 100
```

The output is JSON Lines, one chunk per line:

```
{"source": "manual.pdf", "index": 0, "page": 1, "text": "..."}
```

Errors appear on stderr. The exit code is 1 if at least one file failed and 2 for invalid settings.

### Python API

```python
from doc_chunker import chunk

for c in chunk("manual.pdf", chunk_size=800, overlap=100):
    print(c.index, c.page, c.text)
```

Each chunk has `text`, `source` (file name), `index` (position in the file, from 0) and `page` (page or slide number, otherwise `None`).

Several files, each handled on its own:

```python
from doc_chunker import chunk_many

results = chunk_many(["a.pdf", "b.docx"])
for name, result in results.items():
    if result.ok:
        print(name, len(result.chunks))
    else:
        print(name, "Error:", result.error)
```

If one file fails, the others continue and the error is stored in that file's result.

### How it splits

- Pages and slides are never merged. A Markdown heading always starts a new chunk.
- A section longer than `chunk_size` is split recursively: paragraphs, lines, sentences, words. It only cuts hard when nothing else is left.
- Neighboring chunks share up to `overlap` characters.
- Size is counted in characters, not tokens. No tokenizer is needed.

### What is read

- PDF: text per page. The reading order comes from the position of text blocks, so columns are read one after the other.
- DOCX: paragraphs and tables. Headings become Markdown (`#`, `##`, ...).
- PPTX: text per slide, plus tables and speaker notes.
- TXT and MD: UTF-8 or Latin-1.

### Settings

Order: argument, then environment variable, then default.

| Argument / flag | Environment variable | Default |
| --- | --- | --- |
| `chunk_size` / `--chunk-size` | `DOC_CHUNKER_CHUNK_SIZE` | 1000 characters |
| `overlap` / `--overlap` | `DOC_CHUNKER_OVERLAP` | 150 characters |

`chunk_size` must be at least 50. `overlap` must be smaller than `chunk_size`.

## Limitations

- PDF text is extracted with pdfminer.six. Tables are read column by column. Some PDFs contain icon names as text (for example "briefcase"). Check important results.
- Password protected PDFs are rejected. A PDF without a text layer fails with a message pointing to doc-extract.
- Old formats like DOC and PPT do not work.
- Headers and footers in DOCX are not read.

## Running Tests

```bash
pip install -e ".[test]"
pytest
```

The tests create their own sample files.

## License

MIT
