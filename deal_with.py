#!venv/bin/python3


"""Some functions to deal with the URLs of my rss."""


from src.utilities import StdRedirect
from src.rss_thread import RssThread


dprint = print  # pylint:disable=invalid-name


def do_work():
    """Make the work with the given URL."""
    while 1:
        print("Quelle est l'URL ? ")
        url = input("")
        RssThread(url).start()


StdRedirect()
do_work()
