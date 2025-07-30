import datetime
from typing import Any
from typing import TYPE_CHECKING
from zoneinfo import ZoneInfo

import yt_dlp


from src.exceptions import NoFormatFound
from src.credentials import get_key
from src.utilities import dprint
from src.utilities import print_json
from src.utilities import always_true
from src.utilities import ciao
_: Any = dprint, print_json, ciao, always_true

youtube_dl = yt_dlp
if TYPE_CHECKING:
    from src.yt_video import YtVideo


def build_cookies_arg():
    """Return the cookie part of yt-dlp command line."""
    ff_profile_path = get_key('ff_profile_path')
    return ["--cookies-from-browser", f"firefox:{ff_profile_path}"]


def add_cookies_arg(cmd_list:list[str])->list[str]:
    """Add the cookies args to the yt command."""
    cookies_args = build_cookies_arg()
    arg_name = cookies_args[0]
    arg_value = cookies_args[1]
    cmd_list.insert(1,arg_name)
    cmd_list.insert(2,arg_value)
    return cmd_list


def sanitize_yt_url(url: str) -> str:
    """Remove the part after the first '&'"""
    if not url.startswith("https"):
        if len(url) != 11:
            raise ValueError(f"Si c'est un code, il n'est pas complet : {url}")
        url = f"https://www.youtube.com/watch?v={url}"
    pos = url.find('&')
    if pos != -1:
        return url[0:pos]
    return url


def sanitize_filename(filename: str) -> str:
    """Remove some problematic characters in the filename"""
    filename = filename.replace(" ", "_")
    filename = filename.replace("/", "_")
    return filename


def is_youtube(video: 'YtVideo'):
    """Say if this is a youtube video."""
    url = video.url
    if "youtube.com" in url:
        return True
    if "youtu.be" in url:
        return True
    return False


def ytdlp_options(video: 'YtVideo'):
    """Return the basic options."""
    ff_profile_path = get_key("ff_profile_path")
    options: dict[str, Any] = {
        'noplaylist': True,
    }
    if is_youtube(video):
        options['cookiesfrombrowser'] = ('firefox', ff_profile_path)
    return options


def is_video_format(j_format: dict[str, Any]):
    """Say if a given format is video."""
    resolution = j_format["resolution"]
    if resolution == "audio only":
        return False
    return True


def get_pixel_size(j_format: dict[str, Any]) -> int:
    """Say the size in pixel square of a format."""
    resolution = j_format['resolution']
    parts = resolution.split("x")
    str_xres = parts[0]
    str_yres = parts[1]
    xres = int(str_xres)
    yres = int(str_yres)
    return xres * yres


def show_format(form: dict[str, Any]):
    """Print a format for me."""
    resolution = form['resolution']
    ext = form['video_ext']
    note = form.get('format_note', None)
    ident = form['format_id']
    print(f"{ident} -> {resolution}, {note}, {ext}")


def get_second_best(formats: list[dict[str, Any]]):
    """Return the second best video format."""
    best = formats[0]
    second_best = formats[0]
    for form in formats:
        if get_pixel_size(form) > get_pixel_size(best):
            second_best = best
            best = form
    return second_best


def select_vid_format(video: 'YtVideo') -> str:
    """Select the video format I want."""
    infos = video.infos
    channel_id = infos.get("channel_id")
    if channel_id == "UCqA8H22FwgBVcF3GJpp0MQw":
        print("Monsieur phi. Je prend résolution max.")
        video.show_formats()
        return "271"

    formats: list[dict[str, Any]] = []
    for j_format in infos['formats']:
        if is_video_format(j_format):
            formats.append(j_format)

    formats.sort(key=lambda x: get_pixel_size(x))

    for j_format in formats:
        show_format(j_format)

    select = get_second_best(formats)
    print("sélectionné:")
    show_format(select)

    return select['format_id']


def is_ok_audio_format(note: str):
    """Say if this is the default autio format."""
    if "original" in note:
        return True
    if "Default" in note:
        return True
    if 'medium' in note:
        return True
    return False


def select_audio_format(video: 'YtVideo'):
    """Return the audio format I want."""
    infos = video.infos

    ok_formats: dict[str, str] = {}
    all_audio: dict[str, str] = {}
    for format_info in infos['formats']:
        ident = format_info.get('format_id', 'id???')
        note = format_info.get('format_note', 'note???')
        all_audio[ident] = note
        if is_ok_audio_format(note):
            ok_formats[ident] = note

    words = ["high", "default", "medium"]
    for word in words:
        for ident, note in ok_formats.items():
            if word in note:
                print(f"[Audio selection] {ident}: {note}")
                return ident

    print("Available audio formats:")
    for ident, note in all_audio.items():
        print(f" {ident}: {note}")

    ciao("Tu dois séléctionner un format audio là-dedans")
    raise NoFormatFound('Pas de bon format audio trouvé')


def filename_timestamp(timestamp:int)->str:
    """Return a human readable ts to be used as filename."""
    zone = ZoneInfo("Europe/Paris")
    dt_object = datetime.datetime.fromtimestamp(timestamp, tz=zone)
    return dt_object.strftime("%d_%b_%Y")
