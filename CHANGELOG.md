# Changelog

All notable changes to this project are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/) and the project uses [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.1.0] - 2026-10-17

### Added

- Reads PDF, DOCX, PPTX, TXT and Markdown.
- PDF text extraction with pdfminer.six. Reading order is derived from block positions, so multi-column pages with headings and footers are read correctly. Tables are read column by column.
- Recursive character splitting with overlap.
- Page, slide and Markdown heading boundaries.
- Library API (`chunk`, `chunk_many`) and `doc-chunker` CLI with JSON Lines output.

[Unreleased]: https://github.com/hamidmergan/doc-chunker/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/hamidmergan/doc-chunker/releases/tag/v0.1.0
