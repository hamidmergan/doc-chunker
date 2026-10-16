import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Union

from .errors import ChunkError, ConfigError
from .loaders import load
from .splitter import split_text

DEFAULT_CHUNK_SIZE = 1000
DEFAULT_OVERLAP = 150

_HEADING = re.compile(r"^#{1,6}\s+\S", re.MULTILINE)


@dataclass
class Chunk:
    text: str
    source: str
    index: int
    page: Optional[int] = None

    def to_dict(self) -> dict:
        return {"source": self.source, "index": self.index, "page": self.page, "text": self.text}


@dataclass
class Result:
    chunks: List[Chunk] = field(default_factory=list)
    error: Optional[str] = None

    @property
    def ok(self) -> bool:
        return self.error is None


def _int_setting(value: Optional[int], env: str, default: int) -> int:
    if value is None:
        raw = os.environ.get(env)
        if raw is None or raw.strip() == "":
            return default
        try:
            value = int(raw)
        except ValueError:
            raise ConfigError(f"{env} must be an integer, got {raw!r}.")
    return value


def _check(chunk_size: int, overlap: int) -> None:
    if chunk_size < 50:
        raise ConfigError("chunk_size must be at least 50 characters.")
    if overlap < 0 or overlap >= chunk_size:
        raise ConfigError("overlap must be between 0 and chunk_size minus 1.")


def _by_heading(text: str) -> List[str]:
    """Split Markdown text before every heading."""
    starts = [m.start() for m in _HEADING.finditer(text)]
    if not starts:
        return [text]
    cuts = sorted(set([0] + starts)) + [len(text)]
    return [text[a:b] for a, b in zip(cuts, cuts[1:]) if text[a:b].strip()]


def chunk(
    path: Union[str, Path],
    chunk_size: Optional[int] = None,
    overlap: Optional[int] = None,
) -> List[Chunk]:
    """Split a file into text chunks.

    A page or slide is never merged with the next one.
    A Markdown heading always starts a new chunk.
    """
    size = _int_setting(chunk_size, "DOC_CHUNKER_CHUNK_SIZE", DEFAULT_CHUNK_SIZE)
    over = _int_setting(overlap, "DOC_CHUNKER_OVERLAP", DEFAULT_OVERLAP)
    _check(size, over)

    path = Path(path)
    chunks: List[Chunk] = []
    for section in load(path):
        for block in _by_heading(section.text):
            for text in split_text(block, size, over):
                chunks.append(Chunk(text, path.name, len(chunks), section.page))
    return chunks


def chunk_many(
    paths: List[Union[str, Path]],
    chunk_size: Optional[int] = None,
    overlap: Optional[int] = None,
) -> Dict[str, Result]:
    """Like chunk, but for several files. One failure does not stop the others."""
    size = _int_setting(chunk_size, "DOC_CHUNKER_CHUNK_SIZE", DEFAULT_CHUNK_SIZE)
    over = _int_setting(overlap, "DOC_CHUNKER_OVERLAP", DEFAULT_OVERLAP)
    _check(size, over)

    results: Dict[str, Result] = {}
    for p in paths:
        key = str(p)
        try:
            results[key] = Result(chunks=chunk(p, size, over))
        except ChunkError as exc:
            results[key] = Result(error=str(exc))
    return results
