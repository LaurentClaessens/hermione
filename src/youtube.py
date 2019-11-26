"""The functions for youtube."""

def from_youtube(url):
    """What I do when the URL is from youtube."""
    ydl_opts = {
        'progress_hooks': [my_hook],
            }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
