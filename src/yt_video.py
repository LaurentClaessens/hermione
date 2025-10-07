from typing import Any
from pathlib import Path

import yt_dlp


import dirmanage
from src.exceptions import LiveEventError
from src.utilities_b import ytdlp_options
from src.utilities_b import sanitize_filename
from src.utilities_b import sanitize_yt_url
from src.utilities_b import filename_timestamp
from src.utilities import ciao
from src.utilities import dprint
_: Any = ciao, dprint

youtube_dl = yt_dlp


class YtVideo:

    def __init__(self, url: str):
        self.url = sanitize_yt_url(url)
        self.infos = self.get_infos()
        self.outfile = self.get_outfile()

    def get_outfile(self) -> Path:
        """Return the file in which we have to output."""
        title = self.infos["title"]
        ext = self.infos['ext']
        vid_id = self.infos['id']
        timestamp = self.infos['timestamp']
        channel = self.infos["channel"]
        base_dir = dirmanage.base_dir / "downloads"
        fn_ts = filename_timestamp(timestamp)
        filename = f"{timestamp}_{fn_ts}_{channel}_{vid_id}_{title}.{ext}"
        filename = sanitize_filename(filename)
        return (base_dir / filename).resolve()

    def get_infos(self) -> dict:
        """Return the informations about the video."""
        ydl_opts = ytdlp_options(self)
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                infos = ydl.extract_info(self.url, download=False)
            except yt_dlp.utils.DownloadError as error:
                str_error = str(error)
                if "This live event will begin" in str_error:
                    raise LiveEventError(str_error)
                print(f"l'erreur vue est : {str_error}")
                raise
        if infos is None:
            raise TypeError("Connot download the infos")
        return infos

    def show_formats(self):
        """Show the availabe formats."""
        options = ytdlp_options(self)
        more_options = {
            'outtmpl': '%(id)s',
            'listformats': True,
        }
        options.update(more_options)

        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([self.url])
