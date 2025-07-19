#!venv/bin/python3

import sys
import yt_dlp
from src.utilities_b import get_channel_id

youtube_dl = yt_dlp

"""Return the RSS url from the url of a video."""


def do_work():
    """Make the work."""
    url = sys.argv[1]
    channel_id = get_channel_id(url)

    base = 'https://www.youtube.com/feeds/videos.xml?channel_id'
    print("\n"*3)
    print(f'{base}={channel_id}')


do_work()
