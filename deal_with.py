#!venv/bin/python3


"""Some functions to deal with the URLs of my rss."""

import sys
from lxml import html
import requests
import youtube_dl


from utilities import cache_or_download

def from_youtube(url):
    """What I do when the URL is from youtube."""
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def from_smbc(url):
    """Make the work for smbc."""
    content = cache_or_download(url)
    tree = html.fromstring(content)

    div = tree.xpath('//div[@id="cc-comicbody"]')[0]
    print(div, type(div), dir(div))
    print(div.attrib)
    img = div.xpath('//img')
    print(img.attrib)

def do_work():
    """Make the work with the given URL."""
    url = sys.argv[1]
    if "youtube.com" in url:
        from_youtube(url)
    if "smbc" in url:
        from_smbc(url)

do_work()
