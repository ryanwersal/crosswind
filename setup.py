#!/usr/bin/env python2.7

#Thanks to srid for this next bit:
import sys
print ("Checking Python version info..."),
if sys.version_info < (2, 7) or sys.version_info >= (3, 0):
    sys.exit("ERROR: 3to2 requires at least Python 2.7 in the 2.x branch.")
else:
    print ("%d.%d.%d" % (sys.version_info[:3]))

from distutils.core import setup

setup(
   name="3to2",
   packages=["lib3to2","lib3to2.fixes","lib3to2.tests"],
   scripts=["3to2"],
   version="0.1a2",
)
