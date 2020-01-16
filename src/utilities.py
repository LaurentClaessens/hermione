"""Some utilities."""

import sys
import json
import threading
from pathlib import Path

import hashlib
import requests


dprint = print  # pylint:disable=invalid-name


def write_json_file(json_dict, filename):
    """Write the json dictionary in a file."""
    dump = json.dumps(json_dict, indent=4)

    with open(filename, 'w') as json_file:
        json_file.write(dump)


class WarningContext:
    """Add some indent to 'print'."""

    def __init__(self, title):
        """Initialize."""
        self.title = title
        self.old_stdout = None

    def write(self, text):
        """Write the text with an identation."""
        new_text = "   " + text
        if self.old_stdout:
            self.old_stdout.write(new_text)
        else:
            print(new_text)

    def __enter__(self):
        """
        Enter the context manager.

        Get stdout.
        """
        print(self.title)
        self.old_stdout = sys.stdout
        sys.stdout = self

    def __exit__(self, *exc):
        """Exit the context manager"""
        sys.stdout = self.old_stdout


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
