#!venv/bin/python3
"""Resize a video."""

from pathlib import Path


import cv2

import dirmanage
from src.utilities import ciao

SMALL_TARGET = 960  # Sufficient for my usage


def get_scale_for_small(small_target: int, height: float, width: int):
    """Say the scale factor to get the smallest side as requested."""
    current_small = min(height, width)
    return small_target / current_small


def get_video_size(filepath: Path):
    """Return the (height, width) of a video."""
    vid = cv2.VideoCapture(str(filepath))
    height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)

    return int(height), int(width)


def get_ffmpeg_scale(height: int, width: int, small_target: int) -> str | None:
    """Give the scale string for ffmpeg to get the smallest side as the target."""
    smallest = min(height, width)
    if smallest <= small_target:
        return None
    if height <= width:
        return f"scale={small_target}:-1"
    return f"scale=-1:{small_target}"


def resize_video(filepath: Path, ffmpeg_scale: str, dest_path: Path):
    """Resize the given video."""
    command = f'ffmpeg -i {filepath} -vf "{ffmpeg_scale}" {dest_path}'
    print(command)


def do_work():
    ok_suffixes = [".mp4", ".mkv"]
    for elem in dirmanage.base_dir.iterdir():
        if elem.stem.startswith("res_"):
            continue
        if elem.suffix not in ok_suffixes:
            continue
        height, width = get_video_size(elem)
        ffmpeg_scale = get_ffmpeg_scale(height, width, 960)
        if not ffmpeg_scale:
            # La définition de la vidéo est déjà plus basse que le minimum.
            continue
        print("\n"*5)
        print(elem)
        print(height, width)
        new_filename = f"resized_{elem.name}"
        new_filepath = dirmanage.base_dir / new_filename
        resize_video(elem, ffmpeg_scale, new_filepath)
        # ciao()


do_work()
