#!venv/bin/python3


"""
Download a video from youtube.

./yt url -22 to get max definition
"""

import sys
import youtube_dl
from src.utilities import WarningContext


dprint = print  # pylint:disable=invalid-name


def is_okay(video_format):
    """
    Say if a video format is okay.

    It has to contain the video and the sound.
    """
    if "only" in video_format["format"]:
        return False
    if not video_format.get('asr', True):
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
            size = video_format.get('filesize', -1)
            format_desc = video_format['format']
            format_list.append(format_id)
            with WarningContext(format_id):
                print(f"format {format_desc}")
                print(f"filesize {size}")

    int_formats = [int(vid) for vid in format_list]

    if "-22" in sys.argv:
        print("I choose the format 22")
        return 22
    if 18 in int_formats:
        print("I choose the format 18")
        return 18
    print("")
    format_number = input(f"What format do you want {int_formats} ? ")
    return format_number


def download(url, format_number):
    """Download the video."""
    format_number = str(format_number)
    ydl_opts = {
        'format': format_number,
        'noplaylist': True}

    print("")
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    print("Done.")


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
    video_format = ask_format(url)
    download(url, video_format)


do_work()
