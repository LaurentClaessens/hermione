#!venv/bin/python3


"""Some functions to deal with the URLs of my rss."""


from src.utilities import StdRedirect
from src.utilities import WarningContext
from src.rss_thread import RssThread


dprint = print  # pylint:disable=invalid-name


class Main:
    """The main loop."""
    
    def __init__(self):
        """Initialize."""
        self.thread_list = []

    def new_thread(self, url):
        """Create a new thread for the given URL."""
        rss_thread = RssThread(url)
        rss_thread.rss_write("\n")
        rss_thread.rss_write("----- new -----")
        rss_thread.rss_write("\n")
        rss_thread.start()
        self.thread_list.append(rss_thread)

    def do_work(self):
        """Make the work with the given URL."""
        while 1:
            print("Quelle est l'URL ? ")
            url = input("")
            with WarningContext("Current url"):
                print(url)
                for rss_thread in self.thread_list[:]:
                    print(rss_thread.url)

            if url:
                self.new_thread(url)

            for rss_thread in self.thread_list[:]:
                if not rss_thread.check():
                    self.thread_list.remove(rss_thread)
                    self.new_thread(rss_thread.url)
                if rss_thread.finished:
                    self.thread_list.remove(rss_thread)


StdRedirect()
Main().do_work()
