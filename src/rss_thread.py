"""Describe a thread working on a RSS url."""

from pathlib import Path
import threading


from src.smbc import from_smbc
from src.youtube import from_youtube
from src.utilities import hash_text


class RssThread(threading.Thread):
    """The thread dealing with a RSS url."""

    def __init__(self, url):
        """Initialize."""
        threading.Thread.__init__(self)
        self.url = url
        self.log_file = Path('.').resolve() \
            / "logs" \
            / f"{hash_text(self.url)}.log"
        print(f"Will write in the log file {self.log_file}")

    def rss_write(self, text):
        """Catch the print of the current thread."""
        with open(self.log_file, 'a') as logfile:
            logfile.write(text)

    def flush(self):
        """Implement the flush."""

    def run(self):
        """Make the work."""
        if "youtube.com" in self.url:
            from_youtube(self.url)
        if "smbc" in self.url:
            from_smbc(self.url)
