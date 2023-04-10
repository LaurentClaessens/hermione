"""The functions for youtube."""

import youtube_dl


class FromYoutube:
    """Manage the youtube download."""
    def __init__(self, url, thread):
        """Initialize. Keep a hand on the current thread."""
        self.url = url
        self.thread = thread

    def debug(self, msg):
        """
        Log the debug from youtube-dl.

        This function also catches the string 
        'has already been downloaded and merged'
        because it is the signal that the whole process is finished.
        """
        print('debug')
        key_string = 'has already been downloaded and merged'
        print('   ' + msg)
        if key_string in msg:
            self.thread.finished = True

    def warning(self, msg):
        """Log the warning messages from youtube-dl."""
        print('warning')
        print('   ' + msg)

    def error(self, msg):
        """Log the error messages from youtube-dl."""
        print('error')
        print('   ' + msg)

    def progress_hook(self, data):
        """Progress in youtube-dl."""
        # Using 'WarningContext' here causes reals bugs.
        print("Status report:")
        print(f"   filename: {data['filename']}")
        print(f"   status: {data['status']}")

    def start(self):
        """What I do when the URL is from youtube."""
        ydl_opts = {
            'progress_hooks': [self.progress_hook],
            'logger':self
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.url])
