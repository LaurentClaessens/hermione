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
        return 22

    print("")
    num_list = []
    video_formats = []
    for video_format in infos["formats"]:
        if not is_okay(video_format):
            continue
        video_formats.append(video_format)
        format_id = video_format['format_id']
        num_list.append(format_id)

    k_formats = ["18", "231"]
    hls_formats = ["515", "671", "880", "2103", "1231", "1344",
                   "1357", "1388", "1393", "1399", "1530", "1500",
                   "1530", "1541", "1584", "1420", "1605",
                   "1616", "1648", "1723", "1744", "1773", "1821",
                   "1829", "1871", "1932",
                   "2030", "2050", "2087", "2283", "2551", "2686", "3406"
                   "3470" "3952" "5263"
                   ]
    for hls in hls_formats:
        k_formats.append(f"hls-{hls}-0")
        k_formats.append(f"hls-{hls}-1")

    for num in k_formats:
        if num in num_list:
            print(f"I choose the format {num}")
            return num

    print("rechercher un format qui va bien.")
    bad_formats = []
    for video_format in video_formats:
        format_desc = video_format['format']
        format_id = video_format['format_id']
        with WarningContext(format_id):
            x_size, y_size = get_sizes(format_desc)
            if x_size is None:
                bad_formats.append(format_desc)
                continue
            if min([x_size, y_size]) >= 720:
                print("trouvé : ", format_id)
                return format_id
            bad_formats.append(format_desc)

    print("")
    print("")
    print("")
    print("Suitable format not found")
    print(bad_formats)
    print("")
    print("")
    print("")
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
        pass

    print("Done.")
