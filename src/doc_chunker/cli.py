import argparse
import json
import sys
from pathlib import Path
from typing import List, Optional

from . import __version__
from .core import chunk_many
from .errors import ConfigError


def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="doc-chunker",
        description="Split PDF, DOCX, PPTX, TXT and Markdown into text chunks for RAG. "
        "Output is JSON Lines, one chunk per line.",
    )
    p.add_argument("files", nargs="+", help="input files")
    p.add_argument("-o", "--output", help="output file for one input, folder for several")
    p.add_argument("--chunk-size", type=int, help="maximum characters per chunk (default 1000)")
    p.add_argument("--overlap", type=int, help="overlap in characters (default 150)")
    p.add_argument("--version", action="version", version=f"doc-chunker {__version__}")
    return p


def _lines(chunks) -> str:
    return "".join(json.dumps(c.to_dict(), ensure_ascii=False) + "\n" for c in chunks)


def main(argv: Optional[List[str]] = None) -> int:
    args = _parser().parse_args(argv)
    try:
        results = chunk_many(args.files, args.chunk_size, args.overlap)
    except ConfigError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    out = Path(args.output) if args.output else None
    many = len(args.files) > 1
    if out is not None and many:
        out.mkdir(parents=True, exist_ok=True)

    failed = False
    for name, result in results.items():
        if not result.ok:
            print(f"Error: {result.error}", file=sys.stderr)
            failed = True
            continue
        data = _lines(result.chunks)
        if out is None:
            sys.stdout.write(data)
        elif many:
            (out / (Path(name).name + ".jsonl")).write_text(data, encoding="utf-8")
        else:
            out.write_text(data, encoding="utf-8")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
