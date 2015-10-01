from __future__ import absolute_import, division, unicode_literals

import sys


PY3 = sys.version_info[0] == 3

if PY3:
    iteritems = dict.items

    def execfile(filename, globals, locals):
        with open(filename, 'rb') as fp:
            code = fp.read()
        code = compile(code, filename, 'exec')
        exec(code, globals, locals)
else:
    iteritems = dict.iteritems
    execfile = execfile
