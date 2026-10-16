from typing import List

_SEPARATORS = ["\n\n", "\n", ". ", "! ", "? ", " "]


def _pieces(text: str, size: int, seps: List[str]) -> List[str]:
    """Split text into pieces of up to size characters. The separator stays attached."""
    if len(text) <= size:
        return [text]
    if not seps:
        return [text[i:i + size] for i in range(0, len(text), size)]
    sep, rest = seps[0], seps[1:]
    if sep not in text:
        return _pieces(text, size, rest)
    parts = text.split(sep)
    parts = [p + sep for p in parts[:-1]] + [parts[-1]]
    out: List[str] = []
    for part in parts:
        if not part:
            continue
        if len(part) <= size:
            out.append(part)
        else:
            out.extend(_pieces(part, size, rest))
    return out


def split_text(text: str, chunk_size: int, overlap: int) -> List[str]:
    """Split text into chunks of at most chunk_size characters.

    Splits at paragraphs first, then lines, sentences and words. Only if that
    is not enough does it cut hard. Neighboring chunks overlap by at most
    overlap characters.
    """
    pieces = _pieces(text, chunk_size, _SEPARATORS)
    chunks: List[str] = []
    current: List[str] = []
    length = 0

    def flush() -> None:
        chunk = "".join(current).strip()
        if chunk:
            chunks.append(chunk)

    for piece in pieces:
        if current and length + len(piece) > chunk_size:
            flush()
            tail: List[str] = []
            tail_len = 0
            for prev in reversed(current):
                if tail_len + len(prev) > overlap:
                    break
                tail.insert(0, prev)
                tail_len += len(prev)
            while tail and tail_len + len(piece) > chunk_size:
                tail_len -= len(tail.pop(0))
            current, length = tail, tail_len
        current.append(piece)
        length += len(piece)
    if current:
        flush()
    return chunks
