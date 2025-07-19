import sys
from src.yt_video import YtVideo


def get_channel_id(url: str) -> str:
    """Return the channel id from the url of a video."""
    video = YtVideo(url)
    infos = video.infos

    if not infos:
        print("No information found for {url}")
        sys.exit(1)
    channel_id = infos['channel_id']
    return channel_id
