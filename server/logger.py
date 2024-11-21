import logging
import os
from datetime import datetime

os.makedirs('logs', exist_ok=True)

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
