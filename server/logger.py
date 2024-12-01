import logging
import os
from datetime import datetime

from config import Config

os.makedirs(Config.BOOKMARKS_DIR, exist_ok=True)

timestamp = datetime.now().strftime('%y%m%d%H%M%S')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/{timestamp}.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger()
