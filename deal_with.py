#!venv/bin/python3


"""Some functions to deal with the URLs of my rss."""

import sys
from pathlib import Path
import threading
import youtube_dl



dprint = print


def do_work():
    """Make the work with the given URL."""
    while 1:
        print("Quelle est l'URL ? ")
        url =  input("")
        RssThread(url).start()


StdRedirect()
do_work()
