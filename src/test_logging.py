import config
import logging
from logging.config import fileConfig

#Start logging based on logging.conf
fileConfig('settings/logging.conf')
logger = logging.getLogger()

logging.debug('TEST DEBUG')
logging.info('TEST INFO')
logging.warning('TEST WARNING')
logging.critical('TEST CRITICAL')
