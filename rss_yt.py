#!venv/bin/python3

import sys
import yt_dlp
from src.yt_video import YtVideo
from src.utilities_b import ytdlp_options

youtube_dl = yt_dlp

"""Return the RSS url from the url of a video."""


def do_work():
    """Make the work."""
    url = sys.argv[1]
    video = YtVideo(url)
    ydl_opts = ytdlp_options(video)

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        infos = ydl.extract_info(url, download=False)

    if not infos:
        print("No information found for {url}")
        sys.exit(1)
    channel_id = infos['channel_id']

    base = 'https://www.youtube.com/feeds/videos.xml?channel_id'
    print(f'{base}={channel_id}')


do_work()
