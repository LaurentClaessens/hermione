import yt_dlp


import dirmanage
from src.exceptions import NoFormatFound
from src.credentials import get_key
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


def ytdlp_options():
    """Return the basic options."""
    ff_profile_path = get_key("ff_profile_path")
    return {
        'noplaylist': True,
        'cookiesfrombrowser': ('firefox', ff_profile_path),
    }


def show_formats(infos):
    """Show the availabe formats."""
    for video_format in infos["formats"]:
        print_json(video_format)


def get_infos(url) -> dict:
    """Return the informations about the video."""
    ydl_opts = ytdlp_options()
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        infos = ydl.extract_info(url, download=False)
    if infos is None:
        raise TypeError("Connot download the infos")
    return infos


def select_vid_format(url) -> str:
    """Select the video format I want."""
    infos = get_infos(url)
    channel_id = infos.get("channel_id")
    if channel_id == "UCqA8H22FwgBVcF3GJpp0MQw":
        print("Monsieur phi. Je prend résolution max.")
        ciao("voir ce qu'on peut faire avec ça.")

    my_formats = ["248", "137", "271", "313"]
    available_formats = [form['format_id'] for form in infos['formats']]
    for format_id in my_formats:
        if format_id in available_formats:
            return format_id
    print(available_formats)
    show_formats(infos)
    ciao("Tu dois séléctionner là-dedans")
    raise NoFormatFound('Pas de bon format vidéo trouvé')


def select_audio_format(url):
    """Return the audio format I want."""
    infos = get_infos(url)
    my_formats = ["140", "251", "250", "251-4", "140-5"]
    available_formats = [form['format_id'] for form in infos['formats']]
    for format_id in my_formats:
        if format_id in available_formats:
            return format_id
    print(available_formats)
    show_formats(infos)
    ciao("Tu dois séléctionner un format audio là-dedans")
    raise NoFormatFound('Pas de bon format audio trouvé')


def download(url):
    """Download the video."""
    outfile = dirmanage.base_dir / "downloaded"
    _ = outfile

    audio_format = select_audio_format(url)
    vid_format = select_vid_format(url)
    format_id = f"{vid_format}+{audio_format}"
    print("format sélectionné")
    print(format_id)

    ydl_opts = ytdlp_options()
    ydl_opts["format"] = format_id

    print("")
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:

        print(ydl.get_output_path())
        ydl.download([url])
        pass

    print("Done.")
