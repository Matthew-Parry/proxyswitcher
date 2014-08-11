#!/usr/bin/python

import sys,os
#print("arg1= ")
#print(sys.argv[1])
#print("arg2= ")
#print(sys.argv[2])
#key = sys.argv[1]
#while args:
#    print("export %s=%s" % tuple(args[:2]))
#    del args[:2]
value = ' '.join(sys.argv[2:])
command = 'export %s=%s\n' % ("http_proxy", "dave")
fl =open('settmp.bat', 'w')
os.chmod('settmp.bat', 0o777)
print(command)
fl.write(command)
fl.close()
