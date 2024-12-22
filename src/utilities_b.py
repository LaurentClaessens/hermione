import yt_dlp

from src.exceptions import NoFormatFound
from src.utilities import dprint
from src.utilities import print_json
from src.utilities import ciao
_ = dprint, print_json, ciao

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

    with_audio = video_format['audio_ext']
    if with_audio == "none":
        return False
    format_desc = video_format['format']
    format_id = video_format['format_id']
    x_size, y_size = get_sizes(format_desc)
    if x_size is None:
        return False

    if min([x_size, y_size]) >= 720:
        print("trouvé : ", format_id)
        return True

    return False


def get_sizes(desc: str) -> tuple[int, int]:
    """
    Return the x,y sizes of the format description.
    """
    parts = desc.split(" ")
    for part in parts:
        if "x" not in part:
            continue
        nums = part.split("x")
        x_size = int(nums[0])
        y_size = int(nums[1])
        return x_size, y_size
    return 0, 0


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
        for form in infos["formats"]:
            if form["ext"] != "mp4":
                continue
            number = form["format"]
            resolution = form["resolution"]
            print(f"{number} -> {resolution}")
        # 232, 136 n'ont pas le son
        # avant c'était 22
        return 18

    print("")
    num_list = []
    video_formats = []

    print_json(infos["formats"])

    for video_format in infos["formats"]:
        if not is_okay(video_format):
            continue
        print("ce format semble ok")
        print_json(video_format)
        video_formats.append(video_format)
        format_id = video_format['format_id']
        num_list.append(format_id)

    dprint(f"liste des numéros : {num_list}")
    if not num_list:
        raise NoFormatFound()
    if 18 in num_list:
        return 18
    return num_list[0]


def download(url):
    """Download the video."""
    ydl_opts = {
        'noplaylist': True,
        'language': 'fr'}

    ydl_opts = {
        'noplaylist': True,
    }

    print("")
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        pass

    print("Done.")
