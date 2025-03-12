#!/usr/bin/python3


"""
Get the url of all videos from a yt channel.
- go to the list of videos
- open the inspector
- copy-paste the code in 'channel.html'

This script will give the list of all the urls.

This script is far from being finished.
"""

from pathlib import Path


HREF_TEXT = 'href="/watch?v='


def is_ok_line(line: str):
    if "ytd-playlist-thumbnail" not in line:
        return False
    if "video-title" not in line:
        return False
    if HREF_TEXT not in line:
        return False
    return True


def do_work():
    text = Path("channel.html").read_text()
    lines = text.split("\n")
    ok_lines = [line for line in lines if is_ok_line(line)]
    print(len(ok_lines))

    codes: list[str] = []
    for line in ok_lines:
        print("=======")
        href_pos = line.find(HREF_TEXT)
        trail = line[href_pos+len(HREF_TEXT):]
        print(trail)
        end_pos = trail.find('"><')
        print(line)
        print(trail)
        code = trail[:end_pos]
        print(code)
        codes.append(code)

    print(codes)
    print(len(codes))

    prefix = "https://www.youtube.com/watch?v="
    urls: list[str] = [f"{prefix}{code}" for code in codes]
    for url in urls:
        print(url)


do_work()
