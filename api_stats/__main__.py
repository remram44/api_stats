from __future__ import absolute_import, division, unicode_literals

import os
import sys


try:
    from api_stats.record import main
except ImportError:
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from api_stats.record import main

if __name__ == '__main__':
    main()
