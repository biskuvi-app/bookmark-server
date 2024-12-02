import logging
import os
from datetime import datetime

from config import Config

os.makedirs(Config.LOGS_DIR, exist_ok=True)


class Logger:
    _logger = logging.getLogger()

    def error(self, message):
        now = datetime.now()
        file = now.strftime('%y%m%d')
        pref = now.strftime('%H%M%S')
        with open(f"{Config.LOGS_DIR}/{file}.log", "a") as f:
            f.write(f"{pref} {message}\n")
        self._logger.error(message)


logger = Logger()
