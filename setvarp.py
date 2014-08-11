#!/usr/bin/python

import sys
args = sys.argv[1:]
while args:
    print("export %s=%s" % tuple(args[:2]))
    del args[:2]
#value = eval(' '.join(sys.argv[2:]))
#command =  'set %s=%s\n' % (key, value)
#open('settmp.bat', 'w').write(command)
