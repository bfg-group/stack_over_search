import logging
from configparser import ConfigParser
import os


def stack_logger():
    config = ConfigParser()

    config.read('/etc/stackoversearch/stack_settings.ini')

    logfile = config.get('logs', 'path')
    loglevel = config.get('logs', 'level').upper()

    level = get_log_level(loglevel)

    if not os.path.exists(logfile):
        os.makedirs(logfile)

    logging.basicConfig(filename=logfile+'/stack_over_search.log',
                        format='[%(asctime)s] - %(lineno)d - %(message)s',
                        level=level)
    logger = logging.getLogger()
    return logger


def get_log_level(loglevel):
    level = logging.DEBUG if loglevel == "INFO" else None
    level = logging.INFO if loglevel == "INFO" else None
    level = logging.ERROR if loglevel == "ERROR" else None
    level = logging.DISASTER if loglevel == "DISASTER" else None
    if level is None:
        level = logging.ERROR
    return level
