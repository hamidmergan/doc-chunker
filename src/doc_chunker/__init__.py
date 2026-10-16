from .core import Chunk, Result, chunk, chunk_many
from .errors import ChunkError, ConfigError, NoTextError, UnsupportedFileError

__version__ = "0.1.0"

__all__ = [
    "Chunk",
    "Result",
    "chunk",
    "chunk_many",
    "ChunkError",
    "ConfigError",
    "NoTextError",
    "UnsupportedFileError",
    "__version__",
]
