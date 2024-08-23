from logging import getLogger

from yaml import full_load

with open('conf/logging.conf.yml', 'r') as f:
    LOGGING_CONFIG = full_load(f)


logger = getLogger('bet_maker')
