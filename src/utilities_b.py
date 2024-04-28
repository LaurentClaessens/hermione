import yt_dlp

from src.utilities import dprint
from src.utilities import WarningContext
from src.exceptions import UnkownFormat
_ = dprint

youtube_dl = yt_dlp


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
    if infos is None:
        raise TypeError("Connot download the infos")

    channel_id = infos.get("channel_id")
    if channel_id == "UCqA8H22FwgBVcF3GJpp0MQw":
        print("Monsieur phi. Je prend résolution max.")
        return 22

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

    k_formats = ["18", "231", "hls-1584-0"]

    for num in k_formats:
        if num in format_list:
            print(f"I choose the format {num}")
            return num

    print("I found no known formats.")
    raise UnkownFormat()


def download(url):
    """Download the video."""
    video_format = ask_format(url)
    format_number = str(video_format)
    ydl_opts = {
        'format': format_number,
        'noplaylist': True}

    print("")
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    print("Done.")
