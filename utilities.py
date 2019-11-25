"""Some utilities."""

from pathlib import Path
import hashlib


def hash_text(text):
    """Return a hash of the given text."""
    hasher = hashlib.sha256()
    hasher.update(text)
    return hasher.digest()

def cache_or_download(url):
    """Return the content of the URL, or the cache file."""

    content = requests.get(url).content
