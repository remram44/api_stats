from __future__ import absolute_import, division, unicode_literals

import argparse
from datetime import datetime
import json
import locale
from matplotlib.dates import date2num, MonthLocator, DayLocator, DateFormatter
import matplotlib.pyplot as plt
import re
import sys

from api_stats import setup_logging, logger
from api_stats.utils import PY3, iteritems


def parse_date(s):
    try:
        return datetime.strptime(s, '%Y-%m-%dT%H:%M:%S.%f')
    except ValueError:
        return datetime.strptime(s, '%Y-%m-%dT%H:%M:%S')


def main():
    """Entry point when called on the command-line.
    """
    # Locale
    locale.setlocale(locale.LC_ALL, '')

    parser = argparse.ArgumentParser(
        description="api_stats.plot displays the recorded data using "
                    "matplotlib")
    parser.add_argument('-v', '--verbose', action='count', default=1,
                        dest='verbosity',
                        help="augments verbosity level")
    parser.add_argument('-m', action='append', dest='maps', nargs=2,
                        default=[], help="map input data to a plot")
    parser.add_argument('data', help="file from which to read the data")

    args = parser.parse_args()

    setup_logging(args.verbosity)

    # Compile mappings
    maps = [(re.compile(r_from), r_to) for r_from, r_to in args.maps]

    lines = {}  # dict(key:str, dict(date:str, value:float))

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
            date = data['date']
            for key, value in iteritems(data['values']):
                for r_from, r_to in maps:
                    new_key, subs = r_from.subn(r_to, key)
                    if subs:
                        logger.debug("MAP: %s -> %s", key, new_key)
                        assert isinstance(value, (long, int, float))
                        this_line = lines.setdefault(new_key, {})
                        this_line[date] = this_line.get(date, 0) + value
        logger.info("Read %d lines", nb_lines)
    finally:
        fp.close()

    plots = {}  # dict(title:str, dict(key:tuple, dict(date:str, value:float)))

    for key, values in iteritems(lines):
        key = key.split(':')
        if len(key) > 1:
            title = key[0]
            key = key[1:]
        else:
            title = None
        plots.setdefault(title, {})[tuple(key)] = values

    for title, plot in iteritems(plots):
        logger.info("Creating figure %s", title)
        fig = plt.figure()
        graph = fig.add_subplot(111)
        plt.title(title)
        for key, line in iteritems(plot):
            label = ':'.join(key)
            logger.info("Plotting %s", label)
            x = []
            y = []
            for k, v in sorted((date2num(parse_date(k)), v)
                               for k, v in iteritems(line)):
                x.append(k)
                y.append(v)
            graph.plot(x, y, '-o', label=label)
            graph.xaxis.set_major_locator(MonthLocator())
            graph.xaxis.set_minor_locator(DayLocator())
            graph.xaxis.set_major_formatter(DateFormatter('%Y-%m'))
            graph.legend()

    plt.show()


if __name__ == '__main__':
    main()
