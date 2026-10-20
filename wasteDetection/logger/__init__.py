import logging
import os
from datetime import datetime

try:
    from from_root import from_root
    ROOT_DIR = from_root()
except Exception:
    ROOT_DIR = os.getcwd()

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
log_dir = os.path.join(ROOT_DIR, 'log')
os.makedirs(log_dir, exist_ok=True)

LOG_FILE_PATH = os.path.join(log_dir, LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format='[%(asctime)s] %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)