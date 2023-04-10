"""Describe a thread working on a RSS url."""

from pathlib import Path
import threading


from src.smbc import from_smbc
from src.youtube import FromYoutube
from src.utilities import hash_text
from src.utilities import WarningContext


class RssThread(threading.Thread):
    """The thread dealing with a RSS url."""

    def __init__(self, url):
        """Initialize."""
        threading.Thread.__init__(self)
        self.url = url
        self.finished = False
        self.log_file = Path('.').resolve() \
            / "logs" \
            / f"{hash_text(self.url)}.log"
        print(f"Will write in the log file {self.log_file}")

    def check(self):
        """Check if self is alive and restart if needed."""
        with WarningContext(f"Check thread {self.url}"):
            print(f"url: {self.url}")
            print(f"alive: {self.is_alive()}")
            print(f"finished: {self.finished}")
            if self.is_alive():
                return True
            if self.finished:
                return True
            print(f"I'm going to restart.")
            return False

    def rss_write(self, text):
        """Catch the print of the current thread."""
        with open(self.log_file, 'a') as logfile:
            logfile.write(text)

    def flush(self):
        """Implement the flush."""

    def run(self):
        """Make the work."""
        if "youtube.com" in self.url:
            FromYoutube(self.url, self).start()
        if "smbc" in self.url:
            from_smbc(self.url)
