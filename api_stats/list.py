from __future__ import absolute_import, division, unicode_literals

import argparse
import json
import locale
import sys

from api_stats import setup_logging, logger
from api_stats.utils import PY3, iteritems


def print_tree(keys, level=0):
    """Print keys in a nested dictionary structure.
    """
    for k, v in sorted(iteritems(keys)):
        print("%s%s" % ("  " * level, k))
        print_tree(v, level + 1)


def main():
    """Entry point when called on the command-line.
    """
    # Locale
    locale.setlocale(locale.LC_ALL, '')

    parser = argparse.ArgumentParser(
        description="api_stats.list prints the keys available in the data")
    parser.add_argument('-v', '--verbose', action='count', default=1,
                        dest='verbosity',
                        help="augments verbosity level")
    parser.add_argument('data', help="file from which to read the data")

    args = parser.parse_args()

    setup_logging(args.verbosity)

    keys = {}

    if PY3:
        fp = open(args.data, 'r', encoding='utf-8')
    else:
        fp = open(args.data, 'rb')
    try:
        nb_lines = 0
        for line in fp:
            if not line:
                continue
            nb_lines += 1
            data = json.loads(line)
            if data['format'] != 1:
                logger.critical("Found line in unknown format %r",
                                data['format'])
                sys.exit(1)
            for key, value in iteritems(data['values']):
                key = key.split('/')
                pos = keys
                while key:
                    pos = pos.setdefault(key.pop(0), {})
        logger.info("Read %d lines", nb_lines)
    finally:
        fp.close()

    print_tree(keys)


if __name__ == '__main__':
    main()
