import hashlib
from pathlib import Path


def hash_file(path) -> str:
    """Return a sha256 hex digest of a file's contents, used to detect changed/unchanged PDFs."""
    sha256 = hashlib.sha256()
    with open(Path(path), "rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            sha256.update(block)
    return sha256.hexdigest()
