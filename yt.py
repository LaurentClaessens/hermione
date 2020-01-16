#!venv/bin/python3


"""Download a video from youtube."""

import sys
import youtube_dl
from src.utilities import WarningContext


dprint = print  # pylint:disable=invalid-name



def is_okay(video_format):
    """
    Say if a video format is okay.

    It has to contain the video and the sound.
    """
    if not video_format['asr']:
        return False
    if "only" in video_format["format"]:
        return False
    return True


def ask_format(url):
    """
    Ask for the requested video format.

    @return {string}
        The number of the requested video format.
    """
    ydl_opts = {}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        infos = ydl.extract_info(url, download=False)

    print("")
    format_list = []
    with WarningContext("Here are the available formats"):
        for video_format in infos["formats"]:
            if not is_okay(video_format):
                continue
            format_id = video_format['format_id']
            size = video_format['filesize']
            format_desc = video_format['format']
            format_list.append(format_id)
            with WarningContext(format_id):
                print(f"format {format_desc}")
                print(f"filesize {size}")

    print("")
    int_formats = [int(vid) for vid in format_list]
    format_number = input(f"What format do you want {int_formats} ? ")
    return format_number


def download(url, format_number):
    """Download the video."""
    ydl_opts = {
        'format': format_number,
        'noplaylist' : True}

    print("")
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    print("Done.")


def do_work():
    """Do the work."""
    url = sys.argv[1]
    video_format = ask_format(url)
    download(url, video_format)


do_work()
