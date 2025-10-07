#!venv/bin/python3

"""
Download the files from the content of a text file.

Astuce dans nvim:
    autocmd TextChanged,TextChangedI <buffer> silent write
"""

import sys
import time
import contextlib

import dirmanage
from src.exceptions import LiveEventError
from src.download import download
from src.utilities import random_string
from src.utilities import write_json_file
from src.utilities import print_json
from src.utilities import ColorOutput
from src.exceptions import UnkownFormat
from src.exceptions import AlreadyDownloaded


class Options:

    def __init__(self):
        self.already_submited: list[str] = []
        self.finished: list[str] = []
        self.list_file = dirmanage.init_dir / sys.argv[1]
        filename = f"with_errors_{random_string(5)}.json"
        self.error_file = dirmanage.init_dir / filename
        self.with_error: list[dict[str,str]] = []

    def save_errors(self):
        """Save the file with error urls."""
        write_json_file(self.with_error, self.error_file)


def read_list_file(options: Options):
    """
    Return the content of the text file we are following.

    Since the point of this script is to write in the file in the same 
    time as reading, it happens that the file is being written when
    we read it. This causes FileNotFoundError.
    """
    text = None
    while text is None:
        with contextlib.suppress(FileNotFoundError):
            text = options.list_file.read_text()
    return text


def get_new_urls(options: Options):
    """yield a list of new urls."""
    text = read_list_file(options)
    lines = text.splitlines()
    urls: list[str] = []
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
            urls.append(line)
    return urls


def one_job(url: str):
    """Download and manage the exception."""
    try:
        download(url)
    except UnkownFormat:
        d_error = {"url": url,
                   "error": "unknown format"}
        options.with_error.append(d_error)
        options.save_errors()
    except AlreadyDownloaded:
        pass
    except LiveEventError as error:
        d_error = {"url":url,
                 "error": error.message}
        options.with_error.append(d_error)
    finally:
        options.finished.append(url)


options = Options()

jobs = []
urls:list[str] = []
while True:
    time.sleep(3)
    new_urls = get_new_urls(options)
    urls.extend(new_urls)
    for url in urls:
        print("Errors: ")
        print_json(options.with_error)
        if url in options.already_submited:
            continue
        print(f"{len(options.finished)}/{len(urls)}")
        options.already_submited.append(url)
        one_job(url)
        delay = 30
        print(f"Attendre {delay}s pour ne pas faire peur à Google.")
        time.sleep(delay)  # delay to avoid banishment from yt.
        l_finished = len(options.finished)
        with ColorOutput("green"):
            print(f"Done: {l_finished}/{len(urls)}")
