# Changelog

All notable changes to this project are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/) and the project uses [Semantic Versioning](https://semver.org/).

## [Unreleased]

- PDF: text extraction now uses pdfminer.six (MIT) instead of pypdf. This fixes split letters in many PDFs.
- PDF: reading order is derived from block positions, so multi-column pages with headings and footers are read correctly. Tables are read column by column.

## [0.1.0]

- First release.
- Reads PDF, DOCX, PPTX, TXT and Markdown.
- Recursive character splitting with overlap.
- Page, slide and Markdown heading boundaries.
- Library API (`chunk`, `chunk_many`) and `doc-chunker` CLI with JSON Lines output.
