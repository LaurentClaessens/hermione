from typing import TYPE_CHECKING
from typing import Any

import yt_dlp


from src.exceptions import NoFormatFound
from src.credentials import get_key
from src.utilities import dprint
from src.utilities import print_json
from src.utilities import always_true
from src.utilities import ciao
_ = dprint, print_json, ciao

youtube_dl = yt_dlp

if TYPE_CHECKING:
    from src.yt_video import YtVideo


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
        if not always_true():
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
                  "135"]
    available_formats = [form['format_id'] for form in infos['formats']]
    for format_id in my_formats:
        if format_id in available_formats:
            return format_id
    print(available_formats)
    video.show_formats()
    ciao("Tu dois séléctionner un format vidéo là-dedans")
    raise NoFormatFound('Pas de bon format vidéo trouvé')


def select_audio_format(video: 'YtVideo'):
    """Return the audio format I want."""
    infos = video.infos
    my_formats = ["140", "251", "250", "251-4",
                  "140-5", "140-1", "140-0", "251-0", "250-1"]
    available_formats = [form['format_id'] for form in infos['formats']]
    for format_id in my_formats:
        if format_id in available_formats:
            return format_id
    print(available_formats)
    video.show_formats()
    ciao("Tu dois séléctionner un format audio là-dedans")
    raise NoFormatFound('Pas de bon format audio trouvé')
