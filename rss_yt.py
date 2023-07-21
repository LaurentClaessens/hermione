#!venv/bin/python3

import sys
import yt_dlp

youtube_dl = yt_dlp

"""Return the RSS url from the url of a video."""


def do_work():
    """Make the work."""
    url = sys.argv[1]
    ydl_opts = {}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        infos = ydl.extract_info(url, download=False)
        channel_id = infos['channel_id']
    print(f'https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}')


do_work()
