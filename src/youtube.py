"""The functions for youtube."""

import youtube_dl


def progress_hook(data):
    """Progress in youtube-dl."""
    print(data, type(data))


def from_youtube(url):
    """What I do when the URL is from youtube."""
    ydl_opts = {
        'progress_hooks': [progress_hook],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
