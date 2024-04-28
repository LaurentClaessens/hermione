#!venv/bin/python3

"""Download the files from the content of a text file."""

import sys
import time
from concurrent.futures import ThreadPoolExecutor

import dirmanage
from src.utilities_b import download


class Options:

    def __init__(self):
        self.already_submited: list[str] = []
        self.list_file = dirmanage.init_dir / sys.argv[1]


def get_new_urls(options: Options):
    """yield a list of new urls."""
    text = options.list_file.read_text()
    lines = text.splitlines()
    for line in lines:
        if line not in options.already_submited:
            yield line


options = Options()

jobs = []
with ThreadPoolExecutor(max_workers=10) as executor:
    while True:
        for url in get_new_urls(options):
            options.already_submited.append(url)
            job = executor.submit(download, url)
        time.sleep(1)
