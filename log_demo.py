import os

import logging
logger = logging.getLogger(__name__)

data_dir = 'test_case'

logger.info("this is a test script, writing to: {:}".format(data_dir))

from dedalus.tools.config import config
config['logging']['filename'] = os.path.join(data_dir,'logs/dedalus_log')
config['logging']['file_level'] = 'DEBUG'

if not os.path.exists('{:s}/'.format(data_dir)):
    os.mkdir('{:s}/'.format(data_dir))
logdir = os.path.join(data_dir,'logs')
if not os.path.exists(logdir):
    os.mkdir(logdir)

import dedalus.public as de
logger.debug("debug output test")
logger.info("info logger test")
logger.warning("warning test")
