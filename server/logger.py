import logging
import os
from datetime import datetime

from config import Config

os.makedirs(Config.BOOKMARKS_DIR, exist_ok=True)


class Logger:
    _logger = logging.getLogger()

    def error(self, message):
        now = datetime.now()
        file = now.strftime('%y%m%d')
        pref = now.strftime('%H%M%S')
        self._logger.error(message)
        print(f"{pref} {message}", file=f"{Config.BOOKMARKS_DIR}/{file}.log")
