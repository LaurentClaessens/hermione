#!venv/bin/python3

"""Download the files from the content of a text file."""

import sys
import time
from concurrent.futures import ThreadPoolExecutor

import dirmanage
from src.utilities_b import download
from src.utilities import random_string
from src.utilities import write_json_file
from src.exceptions import UnkownFormat


class Options:

    def __init__(self):
        self.already_submited: list[str] = []
        self.list_file = dirmanage.init_dir / sys.argv[1]
        filename = f"with_errors_{random_string(5)}.json"
        self.error_file = dirmanage.init_dir / filename
        self.with_error: list[str] = []

    def save_errors(self):
        """Save the file with error urls."""
        write_json_file(self.with_error, self.error_file)


def get_new_urls(options: Options):
    """yield a list of new urls."""
    text = options.list_file.read_text()
    lines = text.splitlines()
    for line in lines:
        if line not in options.already_submited:
            print("")
            print("")
            print("")
            print("new url found: ", line)
            print("")
            print("")
            print("")
            print("")
            yield line


def one_job(url: str):
    """Download and manage the exception."""
    try:
        download(url)
    except UnkownFormat:
        options.with_error.append(url)
        options.save_errors()


options = Options()

jobs = []
with ThreadPoolExecutor(max_workers=5) as executor:
    while True:
        for url in get_new_urls(options):
            options.already_submited.append(url)
            job = executor.submit(one_job, url)
        time.sleep(1)
