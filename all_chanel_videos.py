#!venv/bin/python3


"""
Mettre l'url d'une des vidéos de la chaine ici en-bas.
Lancer ce script. Il crée un fichier `vids_UC7_gcs09iThXybpVgjHZ_7g.txt`.
Utiliser le `dl_from_file.py`.
"""

import json
from pathlib import Path
from src.utilities_c import get_channel_id
from src.utilities import write_json_file
from src.utilities import dprint
_ = write_json_file, dprint


HREF_TEXT = 'href="/watch?v='


def is_ok_line(line: str):
    if "ytd-playlist-thumbnail" not in line:
        return False
    if "video-title" not in line:
        return False
    if HREF_TEXT not in line:
        return False
    return True


def do_old_work():
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


def read_dumped(dump_txt: str) -> list:
    """
    Read the dumped file.

    The difficulty is that the dumped file is a concatenation of json files.
    """
    objects = []
    decoder = json.JSONDecoder()
    text = dump_txt.lstrip()  # decode hates leading whitespace
    while text:
        obj, index = decoder.raw_decode(text)
        text = text[index:].lstrip()
        objects.append(obj)
        print(obj)
    return objects


def get_all_urls(dump) -> list[str]:
    """Recursivelly parse the given json and return the urls."""
    answer: list[str] = []
    if isinstance(dump, dict):
        for value in dump.values():
            answer.extend(get_all_urls(value))
        if 'url' in dump:
            url = dump['url']
            answer.append(url)
    if isinstance(dump, list):
        for elem in dump:
            answer.extend(get_all_urls(elem))
    return answer


def is_video_url(url: str) -> bool:
    """Say if an url if a video."""
    prefix = "https://www.youtube.com/watch"
    if url.startswith(prefix):
        return True
    return False


def do_work(vid_url: str):
    """Get the url list of a channel."""
    channel_id = get_channel_id(vid_url)
    channel_url = f'https://www.youtube.com/channel/{channel_id}'
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,  # Don't download, just get URLs
    }
    import yt_dlp

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        dump = ydl.extract_info(channel_url, download=False)
    assert dump is not None
    urls = get_all_urls(dump)
    vid_urls = [url for url in urls if is_video_url(url)]

    txt_list = ""
    for url in vid_urls:
        txt_list += url + "\n"

    out_path = Path(f"vids_{channel_id}.txt")
    out_path.write_text(txt_list)


vid_url = 'https://www.youtube.com/watch?v=7wZPaovDH50'
do_work(vid_url)
