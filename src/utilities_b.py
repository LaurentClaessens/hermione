from typing import TYPE_CHECKING
from typing import Any

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


def select_vid_format(video: 'YtVideo') -> str:
    """Select the video format I want."""
    infos = video.infos
    channel_id = infos.get("channel_id")
    if channel_id == "UCqA8H22FwgBVcF3GJpp0MQw":
        print("Monsieur phi. Je prend résolution max.")
        video.show_formats()
        return "271"

    my_formats = ["248", "137", "271", "313", "298", "303", "299",
                  "788", "398", "247", "243", "136",
                  "135", "234", "614"]
    available_formats = [form['format_id'] for form in infos['formats']]
    for format_id in my_formats:
        if format_id in available_formats:
            return format_id
    video.show_formats()
    print("")
    print(available_formats)
    ciao("Tu dois séléctionner un format vidéo là-dedans")
    raise NoFormatFound('Pas de bon format vidéo trouvé')


def is_ok_audio_format(note: str):
    """Say if this is the default autio format."""
    if "original" not in note:
        return False
    return True


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

    for ident, note in ok_formats.items():
        if "high" in note:
            print(f"[Audio selection] {ident}: {note}")
            return ident

    print("Available audio formats:")
    for ident, note in all_audio.items():
        print(f" {ident}: {note}")

    ciao("Tu dois séléctionner un format audio là-dedans")
    raise NoFormatFound('Pas de bon format audio trouvé')
