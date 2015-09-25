#!/usr/bin/env python
from __future__ import absolute_import, division, unicode_literals

import argparse
from datetime import datetime
import json
import locale
import logging
import requests
import sys


__version__ = '0.1'

logger = logging.getLogger('api_stats')


PY3 = sys.version_info[0] == 3

if PY3:
    iteritems = dict.items
else:
    iteritems = dict.iteritems


class StatisticsRecorder(object):
    """Interface with the "configuration files".
    """
    def __init__(self):
        self.recorded_values = {}

    def record(self, key, value):
        logger.debug("record: %r = %r", key, value)
        self.recorded_values[key] = value

    def get_json(self, url):
        logger.info("Downloading JSON from %s", url)
        return requests.get(url).json()


def process_configuration(data_output, configuration_file):
    """Process a configuration file and update the data.
    """
    stats = StatisticsRecorder()

    try:
        with open(configuration_file, 'rb') as fp:
            code = fp.read()
    except IOError as e:
        logger.critical("Cannot open configuration file: %s", e)
        sys.exit(1)

    env = {'stats': stats}
    if PY3:
        exec(code, env, env)
    else:
        exec('exec code in env, env')
    logger.info("Recorded %d values", len(stats.recorded_values))

    if data_output is None:
        logger.warning("Discarding output as requested")
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("Output was:")
            for key, value in iteritems(stats.recorded_values):
                logger.debug("%s = %r", key, value)
    else:
        if PY3:
            fp = open(data_output, 'w', encoding='utf-8', newline='\n')
        else:
            fp = open(data_output, 'wb')
        try:
            json.dump({'format': 1,
                       'date': datetime.now().isoformat(),
                       'values': stats.recorded_values},
                      fp,
                      ensure_ascii=True,
                      indent=None,
                      sort_keys=True)
            fp.write('\n')
        finally:
            fp.close()


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


def main():
    """Entry point when called on the command-line.
    """
    # Locale
    locale.setlocale(locale.LC_ALL, '')

    parser = argparse.ArgumentParser(
        description="api_stats records the history of some data retrived "
                    "from an API")
    parser.add_argument('-v', '--verbose', action='count', default=1,
                        dest='verbosity',
                        help="augments verbosity level")
    parser.add_argument('-n', '--dry-run', action='store_true',
                        help="don't update the data on disk")
    parser.add_argument('configuration', help="configuration file to process")
    parser.add_argument('data', nargs=argparse.OPTIONAL,
                        help="file to update with the new data")

    args = parser.parse_args()
    if args.data is None and not args.dry_run:
        parser.error("No data file specified (or do you mean to use "
                     "--dry-run?)")
        raise RuntimeError  # unreachable

    setup_logging(args.verbosity)

    process_configuration(None if args.dry_run else args.data,
                          args.configuration)


if __name__ == '__main__':
    main()
