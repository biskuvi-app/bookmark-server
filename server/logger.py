import logging
import os
from datetime import datetime

import config

os.makedirs(config.LOGS_DIR, exist_ok=True)


class Logger:
    _logger = logging.getLogger()

    def error(self, message):
        now = datetime.now()
        file = now.strftime('%y%m%d')
        pref = now.strftime('%H%M%S')
        with open(f"{config.LOGS_DIR}/{file}.log", "a") as f:
            f.write(f"{pref} {message}\n")
        self._logger.error(message)


logger = Logger()
