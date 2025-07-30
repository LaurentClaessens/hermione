import sys
import json
import time
import math
import uuid
import socket
import pickle
import random
import string
import logging
import inspect
import hashlib
import datetime
import threading
import contextlib
from zoneinfo import ZoneInfo
from pathlib import Path

from colorama import Fore, Back, Style

from typing import Any
from typing import Union
from typing import Optional

import configparser

from src.stubs import PathOrStr



class LPriniting:
    """Print every 2 seconds instead of immediately."""

    __instance = None

    @staticmethod
    def has_instance():
        """Return True if the instance is already created."""
        return LPriniting.__instance is not None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if LPriniting.__instance == None:
            LPriniting.__instance = LPriniting()
        return LPriniting.__instance

    def __init__(self):
        self.last_ts = time.time()
        self.text_cache: list[str] = []
        self.caller_thread = threading.current_thread()
        self.print_thread = threading.Thread(target=self.print_all)
        self.print_thread.start()

    def has_to_work(self):
        """Return True if the caller thread is still alive."""
        return self.caller_thread.is_alive()

    def print_all(self):
        """Print all the stored text."""
        while True:
            while not self.text_cache:
                time.sleep(2)
            if not self.has_to_work():
                return
            full_text = "\n" + "\n".join(self.text_cache)
            self.text_cache = []
            logging.info(full_text)

    def lprint(self, text):
        """Store something to print later."""
        self.text_cache.append(str(text))


def lprint(text):
    """Print something later."""
    LPriniting.getInstance().lprint(text)


def lprint_json(json_dict, pretty=True):
    """Print the given json."""
    text = json_to_str(json_dict, pretty, ensure_ascii=False)
    lprint(text)


def is_port_in_use(port: int) -> bool:
    """Say if something is listening on the given port."""
    HOST = "localhost"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        try:
            s.connect((HOST, port))
        except socket.error:
            return False
        else:
            return True


class StdRedirect:
    """Redirect stdout to a file."""

    def __init__(self, text, filename, mode='a'):
        """Initialize."""
        self.filename = Path(filename)
        self.mode = mode
        self.old_stdout = sys.stdout
        self.text = text
        self.filename.parent.mkdir(exist_ok=True, parents=True)
        self.out_file = open(self.filename, self.mode)

    def write(self, text):
        """Make the work of 'print'."""
        self.out_file.write(text)
        self.out_file.flush()

    def __exit__(self, *args):
        """Release the resources: stdout and the out file."""
        _ = args
        self.out_file.close()
        sys.stdout = self.old_stdout

    def __enter__(self):
        """Initiate the redirect."""
        print(f"Output {self.text}: tail -f {self.filename}")
        sys.stdout = self


def human_filesize(filepath):
    """Return a human readable size of the requested file."""
    size = filepath.stat().st_size
    suffix = "B"
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(size) < 1024.0:
            return f"{size:3.1f}{unit}{suffix}"
        size /= 1024.0
    return f"{size:.1f}Yi{suffix}"


def ensure_encoded(text, encoding='utf8'):
    """
    Return the encoded text.

    - If it is already 'byte', leave as it.
    - If not, encode.
    """
    try:
        answer = text.encode(encoding)
    except AttributeError:
        answer = text
    return answer


def get_hash_to_int(text) -> int:
    """Hash the text to int."""
    sha1 = hashlib.sha1()
    text = ensure_encoded(text, 'utf8')
    sha1.update(text)
    return int.from_bytes(sha1.digest(), byteorder='big')


def get_hash_to_uuid(text) -> str:
    """Hash the text to int."""
    my_uuid = uuid.uuid3(uuid.NAMESPACE_X500, text)
    return str(my_uuid)


def get_text_hash(text):
    """Return a hash of the given text."""
    sha1 = hashlib.sha1()
    text = ensure_encoded(text, 'utf8')
    sha1.update(text)
    return sha1.hexdigest()


def get_file_hash(filename):
    """
    Return a hash of the given file.

    @return {string}
        The hex digest of the content of the file.
    """
    with open(filename, 'rb') as my_file:
        content = my_file.read()
    return get_text_hash(content)


def filename_timestamp(now=None):
    """Return a human readable timestamp, but ok for filename."""
    if now is None:
        now = time.time()
    local_time = time.localtime(now)
    stamp = time.strftime("%Z-%A_%Y-%B-%d_%Hh%Mm%Ss", local_time)
    return stamp


def random_string(length):
    """Return a random string of letters of the given length."""
    rn_list = [random.choice(string.ascii_letters) for _ in range(0, length)]
    return "".join(rn_list)


def human_timestamp(timestamp=None):
    """Return a human readable timestamp."""

    if timestamp is None:
        timestamp = time.time()

    if isinstance(timestamp, datetime.datetime):
        dt_object = timestamp
    else:
        zone = ZoneInfo("Europe/Paris")
        dt_object = datetime.datetime.fromtimestamp(timestamp, tz=zone)
    return dt_object.strftime("%Z - %a  %Y/%b/%d, %H:%M:%S")


def json_serial(obj):
    """Serialize the datetime."""
    if isinstance(obj, datetime.datetime):
        timestamp = obj.timestamp()
        return human_timestamp(timestamp)
    with contextlib.suppress(AttributeError):
        return obj.to_json()
    return str(obj)


def json_to_str(json_dict, pretty=False, ensure_ascii=True):
    """Return a string representation of the given json."""
    if pretty:
        return json.dumps(json_dict,
                          sort_keys=True,
                          indent=4,
                          default=json_serial,
                          ensure_ascii=ensure_ascii)
    return json.dumps(json_dict, default=json_serial, ensure_ascii=ensure_ascii)


def print_json(json_dict, pretty=True):
    """Print the given json."""
    text = json_to_str(json_dict, pretty)
    print(text)


dprint_json = print_json


def write_json_file(json_dict,
                    filename,
                    pretty=False,
                    parents=True):
    """Write the dictionary in the given file."""
    filename = Path(filename)
    if parents:
        parent = filename.parent
        parent.mkdir(parents=True, exist_ok=True)
    my_str = json_to_str(json_dict, pretty=pretty)
    filename.write_text(my_str)


def read_json_string(json_string: str):
    """Interpret a string as json."""
    try:
        return json.loads(json_string)
    except json.decoder.JSONDecodeError as err:
        print("JSONDecodeError:", err)
        message = f"Error in the json string: {json_string}"
        raise ValueError(message) from err


def read_json_file(json_path: PathOrStr, default=None):
    """ Return the given json file as dictionary."""
    json_path = Path(json_path)
    if not json_path.is_file():
        if default is None:
            raise ValueError(f"You try to read {json_path}. "
                             f"The file does not exist and you "
                             f"furnished no default.")
        return default
    answer = read_json_string(json_path.read_text())
    return answer


def read_dict_json(json_path: Union[Path, str], default=None) -> dict:
    """Read a json knwon to be a dictionary."""
    json_dict = read_json_file(json_path, default=default)
    if not isinstance(json_dict, dict):
        raise TypeError(f"Not a dictionary: {json_path}")
    return json_dict


def read_list_json(json_path: Union[Path, str], default=None) -> list:
    """Read a json knwon to be a list."""
    json_list = read_json_file(json_path, default=default)
    if not isinstance(json_list, list):
        raise ValueError(f"json file {json_path} is not a list")
    return json_list


class WarningContext:
    """Furnish a context manager for printing impressive warnings."""

    def __init__(self, message, always_visible=False):
        """Initialize with the main message."""
        self.message = message
        self.old_stdout = sys.stdout
        self.already_write = False
        self.always_visible = always_visible

    def write(self, text):
        """
        Catch the `print` inside the context.

        Print a warning and take the power over stdout.
        """
        if not self.already_write:
            try:
                self.old_stdout.write(self.message + '\n')
            except TypeError:
                self.old_stdout.write(str(self.message) + '\n')
            self.already_write = True

        self.old_stdout.write("   " + text)

    def __enter__(self):
        """Will write a message when something is really written."""
        sys.stdout = self
        if self.always_visible:
            self.old_stdout.write(self.message + '\n')
            self.already_write = True

    def __exit__(self, *args):
        """Give back the stdout."""
        _ = args
        sys.stdout = self.old_stdout


class Timer:
    """Furnish a context manager for timing the functions."""

    def __init__(self, message, quiet=False, welcome=False):
        """Initialize with the main message."""
        self.message = message
        self.init_time = 0
        self.end_time = None
        self.elapsed = None
        self.quiet = quiet
        self.welcome = welcome

    def __enter__(self):
        """Will write a message when something is really written."""
        if self.welcome:
            print(f"-- timer -- (start) {self.message} -- "
                  f"{human_timestamp()}")
        self.init_time = time.time()
        return self

    def current(self):
        """Return the elapsed time from the enter."""
        now = time.time()
        return now - self.init_time

    def __call__(self, fun):
        """Make this class a decorator as well."""
        def new_fun(*args, **kwargs):
            with Timer(self.message, welcome=self.welcome):
                return fun(*args, **kwargs)
        return new_fun

    def exit_message(self):
        """Return the message to be displayed on exit."""
        self.elapsed = self.current()
        return f"-- timer -- (finish) {self.message} -- {self.elapsed}"

    def __exit__(self, *args):
        """Compute the elapsed time and print a message."""
        _ = args
        self.end_time = time.time()
        if not self.quiet:
            print(self.exit_message())


def remove_dummy(fun):
    """
    Remove the dummy section in an parsed ini file.

    This decorator is dedicated to the function `read_ini_file`.
    """
    def new_fun(filename, remove_dummy=True):
        """decorated."""
        config = fun(filename, remove_dummy=remove_dummy)

        as_dict = dict(config)

        if remove_dummy:
            if "dummy_section" in as_dict:
                return dict(as_dict["dummy_section"])
        return as_dict
    return new_fun


@remove_dummy
def read_ini_file(filename, remove_dummy=True):
    """
    Return the content of the given ini file.

    This function allows to read ini file without sections.
    """
    _ = remove_dummy
    config = configparser.ConfigParser()
    with contextlib.suppress(configparser.MissingSectionHeaderError):
        config.read(filename)
        return config

    # At this point we know that the ini file has no section.
    # We add one.
    with open(filename, 'r') as ini_file:
        config_string = '[dummy_section]\n' + ini_file.read()
    config = configparser.ConfigParser()
    config.read_string(config_string)
    return config


def human_seconds(total):
    """
    Return a human readable time.

    `total` is a number of seconds and we return xxh:yym:zzs
    """
    hours = math.floor(total / 3600)
    remainder = total - 3600 * hours
    minutes = math.floor(remainder / 60)
    remainder = remainder - 60 * minutes
    seconds = round(remainder)
    return f"{hours}h:{minutes}m:{seconds}s"


def human_remaining(start_time, percent):
    """Say how much time it remains."""
    now = time.time()
    elapsed = now - start_time
    try:
        total_time = 100 * elapsed / percent
    except ZeroDivisionError:
        return "computing..."
    remaining = total_time - elapsed

    remain_txt = human_seconds(remaining)

    return remaining, f"{remain_txt}"


def dprint(*args, **kwargs):
    """Print with color for debug purposes."""
    color = kwargs.pop('color', None)
    with ColorOutput(color):
        print(*args, **kwargs)


def ciao(message=None, color=None):
    """For debug only."""
    if color is None:
        color = "yellow"
    if message:
        with ColorOutput("yellow"):
            print("\n", message, "\n")
    x = random.random()
    if x > 3:
        return "pas possible"

    if LPriniting.has_instance():
        time.sleep(3)
        lprinting = LPriniting.getInstance()
        if lprinting.text_cache:
            lprint("Il y a des choses en attente d'impression.")
            lprint("j'attends un peu avant de finir le ciao")
            time.sleep(3)

    current_frame = inspect.stack()[1]
    current_file = Path(current_frame[1]).resolve()
    current_line = current_frame[2]
    print(f"{current_file}, line {current_line} --> ciao !")

    sys.exit(1)


class ColorOutput:
    """Colored output"""

    def __init__(self, fg: Optional[str] = None, bg: Optional[str] = None):
        """Initialize."""
        self.fg = fg
        self.bg = bg

    def __exit__(self, *args):
        """Reset all the colors"""
        _ = args
        print(Style.RESET_ALL)

    def __enter__(self):
        """Initiate the requested color."""
        fg_correspondance = {
            "black": Fore.BLACK,
            "red": Fore.RED,
            "green": Fore.GREEN,
            "yellow": Fore.YELLOW,
            "blue": Fore.BLUE,
            "magenta": Fore.MAGENTA,
            "cyan": Fore.CYAN,
            "white": Fore.WHITE
        }
        bg_correspondance = {
            "black": Back.BLACK,
            "red": Back.RED,
            "green": Back.GREEN,
            "yellow": Back.YELLOW,
            "blue": Back.BLUE,
            "magenta": Back.MAGENTA,
            "cyan": Back.CYAN,
            "white": Back.WHITE}

        if self.fg:
            print(fg_correspondance[self.fg])
        if self.bg:
            print(bg_correspondance[self.bg])

    def __call__(self, fun):
        """Turn the color outpus to a context manager"""
        def wrapper(*args, **kwargs):
            """Wrap the function."""
            with self:
                return fun(*args, **kwargs)
        return wrapper


def deprecation(message=None):
    """Indicate that I think that a function is deprecated."""
    import traceback
    print("Ceci est déprécié.")
    with ColorOutput("magenta"):
        traceback.print_stack(file=sys.stdout)
    ciao(message, color="cyan")


def write_pickle_file(obj, pickle_path: Path):
    """Write the object in a pickle file."""
    pickle_path.parent.mkdir(parents=True, exist_ok=True)
    pickle_path.write_bytes(pickle.dumps(obj))


def read_pickle_file(pickle_path: Path) -> Any:
    """Read the object from the pickle file."""
    try:
        return pickle.loads(pickle_path.read_bytes())
    except EOFError:
        raise EOFError(f"Error in the pickle file: {pickle_path}")


class retry:
    """A retry decorator."""

    def __init__(self, max_retry: int, exceptions: list):
        """Initialize."""
        self.max_retry = max_retry
        self.exceptions = exceptions

    def __call__(self, fun):
        """Make this class a decorator"""
        def wrapper(*args, **kwargs):
            """Wrap the function."""
            for num in range(self.max_retry):
                num += 1
                try:
                    answer = fun(*args, **kwargs)
                except tuple(self.exceptions) as err:
                    print(f"Error: {err}")
                    print("je recommence.")
                    continue
                else:
                    if num > 1:
                        print(f"success after {num} attempts.")
                    return answer
        return wrapper


def always_true():
    """Return True tricking the linter."""
    x = random.random()
    if x < 3:
        return True
    raise ValueError("Should never happen.")
