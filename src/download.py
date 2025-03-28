import contextlib
import subprocess

import yt_dlp


import dirmanage
from src.yt_video import YtVideo
from src.utilities_b import select_audio_format
from src.utilities_b import select_vid_format
from src.utilities_b import ytdlp_options
from src.utilities import write_json_file
from src.utilities import ciao
_ = ciao

youtube_dl = yt_dlp


def download(url):
    """Download the video."""
    video = YtVideo(url)

    write_json_file(video.infos, "infos.json")
    outfile = video.outfile

    audio_format = select_audio_format(video)
    vid_format = select_vid_format(video)
    format_id = f"{vid_format}+{audio_format}"
    print(f"format sélectionné: {format_id}")

    ydl_opts = ytdlp_options(video)
    ydl_opts["format"] = format_id

    print("")
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("out : ", ydl.get_output_path())
        bin_dir = dirmanage.base_dir / "venv" / "bin"
        with contextlib.chdir(bin_dir):
            cmd_list = ["./yt-dlp",
                        url,
                        "--format",
                        format_id,
                        "-o",
                        str(outfile)]

            print(cmd_list)

            subprocess.run(cmd_list)
        # ydl.download([url])

    print("Done.")
