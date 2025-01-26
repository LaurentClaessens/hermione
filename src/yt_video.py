import yt_dlp

from src.utilities_b import ytdlp_options

youtube_dl = yt_dlp


class YtVideo:

    def __init__(self, url: str):
        self.url = url
        self.infos = self.get_infos()

    def get_infos(self) -> dict:
        """Return the informations about the video."""
        ydl_opts = ytdlp_options()
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            infos = ydl.extract_info(self.url, download=False)
        if infos is None:
            raise TypeError("Connot download the infos")
        return infos

    def show_formats(self):
        """Show the availabe formats."""
        options = ytdlp_options()
        more_options = {
            'outtmpl': '%(id)s',
            'listformats': True,
        }
        options.update(more_options)

        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([self.url])
