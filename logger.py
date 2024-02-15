import os
import logging
from logging.handlers import RotatingFileHandler



logging.basicConfig(
    level=logging.DEBUG,
    filename='logs/program.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s - %(name)s'
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(
    os.path.expanduser('logs/bot_log.log'),
    maxBytes=50000000,
    backupCount=5
)
logger.addHandler(handler)