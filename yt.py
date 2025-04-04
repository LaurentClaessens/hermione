#!venv/bin/python3


"""Download a video from youtube."""

import sys
import yt_dlp

from src.download import download

youtube_dl = yt_dlp


def get_url(arg):
    """Build the URL from the argument."""
    if arg.startswith("https"):
        return arg
    else:
        return f"https://youtu.be/{arg}"


def do_work():
    """Do the work."""
    url = get_url(sys.argv[1])
    url = sys.argv[1]
    download(url)


do_work()
