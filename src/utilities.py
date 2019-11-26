"""Some utilities."""


import hashlib
import requests
from pathlib import Path


dprint = print


def hash_text(text):
    """Return a hash of the given text."""
    hasher = hashlib.sha256()
    text = text.encode()
    hasher.update(text)
    return hasher.hexdigest()


def cache_or_download(url):
    """Return the content of the URL, or the cache file."""
    filename = Path('.').resolve() \
        / "cache" \
        / hash_text(url)
    if filename.is_file():
        print(f"read cache: ", filename)
        with open(filename, 'rb') as cached_file:
            return cached_file.read()

    content = requests.get(url).content
    with open(filename, 'wb') as cached_file:
        print(f"write cache: ", filename)
        cached_file.write(content)
    return content

class StdRedirect:
    """Redirect stdout."""

    def __init__(self):
        """Initialize."""
        self.old_stdout = sys.stdout
        sys.stdout = self

    def flush(self):
        """Implement the flush."""
        try:
            threading.current_thread().flush()
        except AttributeError:
            self.old_stdout.flush()

    def write(self, text):
        """Catch the print commands."""
        try:
            threading.current_thread().rss_write(text)
        except AttributeError:
            self.old_stdout.write(text)
