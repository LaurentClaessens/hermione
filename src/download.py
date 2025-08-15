from typing import Any
from pathlib import Path
import contextlib
import subprocess

import yt_dlp


import dirmanage
from src.yt_video import YtVideo
from src.exceptions import DlError
from src.utilities_b import add_cookies_arg
from src.utilities_b import select_audio_format
from src.utilities_b import select_vid_format
from src.utilities_b import ytdlp_options
from src.utilities import write_json_file
from src.utilities import ciao
_:Any = ciao

youtube_dl = yt_dlp



def select_format(video:YtVideo)->str:
    """Select the video format."""

    infos = video.infos
    channel_id = infos.get("channel_id")
    if channel_id == "UCqA8H22FwgBVcF3GJpp0MQw":
        print("Monsieur phi. Je prend résolution max.")
        video.show_formats()
        return '625+234-1'

    print("[select audio format]")
    audio_format = select_audio_format(video)
    print(f"audio selected: {audio_format}")
    print("[select video format]")
    vid_format = select_vid_format(video)
    print(f"video selected: {vid_format}")

    format_id = f"{vid_format}+{audio_format}"
    return format_id


def is_ok_output_file(outfile:Path)->bool:
    """Say if the output file seems ok."""
    if not outfile.is_file():
        return False
    size = outfile.stat().st_size
    mo_size = size/1024**2
    if mo_size < 2:
        # There are probably no video less than 2Mo
        return False
    return True


def download(url: str):
    """Download the video."""
    video = YtVideo(url)

    write_json_file(video.infos, "infos.json", pretty=True)
    outfile = video.outfile

    format_id = select_format(video)

    print(f"format sélectionné: {format_id}")

    ydl_opts = ytdlp_options(video)
    ydl_opts["format"] = format_id

    print("")
    with youtube_dl.YoutubeDL(ydl_opts):
        bin_dir = dirmanage.base_dir / "venv" / "bin"

        with contextlib.chdir(bin_dir):
            cmd_list = ["./yt-dlp",
                        url,
                        "--format",
                        format_id,
                        "-o",
                        str(outfile)]
            cmd_list = add_cookies_arg(cmd_list)

            print(cmd_list)

            subprocess.run(cmd_list)
            if not is_ok_output_file(outfile):
                raise DlError(f"Error when downloading {outfile}")

    print("")
    print("Done.")
    print("")
    print(outfile.name)
