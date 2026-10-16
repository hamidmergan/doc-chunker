class ChunkError(Exception):
    """Base class for all errors in this package."""


class ConfigError(ChunkError):
    """A setting is invalid."""


class UnsupportedFileError(ChunkError):
    """The file type is not supported or the file cannot be read."""


class NoTextError(ChunkError):
    """The file has no extractable text, for example a scan."""
