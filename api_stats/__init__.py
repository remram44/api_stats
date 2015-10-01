from __future__ import absolute_import, division, unicode_literals

import logging


__version__ = '0.3'


logger = logging.getLogger('api_stats')


def setup_logging(verbosity):
    """Sets up the logging module to log to the console.
    """
    levels = [logging.CRITICAL, logging.WARNING, logging.INFO, logging.DEBUG]
    level = levels[min(verbosity, len(levels) - 1)]

    # Formatter
    fmt = "%(asctime)s %(levelname)s: %(message)s"
    formatter = logging.Formatter(fmt)

    # Console logger
    handler = logging.StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(formatter)

    logging.root.setLevel(level)
    logging.root.handlers = []
    logging.root.addHandler(handler)
