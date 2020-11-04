#!venv/bin/python3

import sys

"""Provide the RSS link of a youtube channel."""


def do_work():
    """Make the work."""
    channel = sys.argv[1]
    print(f'https://www.youtube.com/feeds/videos.xml?channel_id={channel}')

do_work()
