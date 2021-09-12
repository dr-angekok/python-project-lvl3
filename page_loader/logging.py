import logging
from sys import stderr

LEVELS = {'debug': logging.DEBUG,
          'warning': logging.WARNING,
          'error': logging.ERROR,
          'critical': logging.CRITICAL,
          'info': logging.INFO}


def setup(log_level):
    """Setting up logging.

    Args:
        log_level (str): 'debug', 'info', 'warning', 'error', 'critical'
    """
    logging.basicConfig(level=LEVELS[log_level])
    logging.StreamHandler(stderr)
