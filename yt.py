#!venv/bin/python3


"""Download a video from youtube."""


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

    for video_format in infos["formats"]:
        if not is_okay(video_format):
            continue
        with WarningContext(video_format['format_id']):
            print(f"format {video_format['format']}")
            print(f"filesize {video_format['filesize']}")

    format_number = input("What format do you want ? ")
    return format_number


def download(url, format_number):
    """Download the video."""
    ydl_opts = {
        'format': format_number,
        'noplaylist' : True}

    print("Vais télécharger ", url)
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    print("Done.")


def do_work():
    """Do the work."""
    url = "https://www.youtube.com/watch?v=fkb1G4RPwwU"
    video_format = ask_format(url)
    download(url, video_format)

do_work()
