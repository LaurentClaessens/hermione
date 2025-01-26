import yt_dlp

from src.yt_video import YtVideo
from src.utilities_b import select_audio_format
from src.utilities_b import select_vid_format
from src.utilities_b import ytdlp_options

youtube_dl = yt_dlp


def download(url):
    """Download the video."""
    video = YtVideo(url)

    audio_format = select_audio_format(video)
    vid_format = select_vid_format(video)
    format_id = f"{vid_format}+{audio_format}"
    print("format sélectionné")
    print(format_id)

    ydl_opts = ytdlp_options()
    ydl_opts["format"] = format_id

    print("")
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print(ydl.get_output_path())
        ydl.download([url])

    print("Done.")
