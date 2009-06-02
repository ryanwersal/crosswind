#!/usr/bin/env python2.7
"""Tests that run all fixer modules over an input stream.

This has been broken out into its own test module because of its
running time.
"""

# Python imports
import unittest
import os.path
import os
from itertools import chain

# Local imports
from lib2to3 import pytree
from lib2to3 import refactor
from lib2to3.tests import support
from lib2to3.tests.test_fixers import FixerTestCase

class lib3to2FixerTestCase(FixerTestCase):
    def setUp(self, fix_list=None, fixer_pkg="lib3to2"):
        super(lib3to2FixerTestCase, self).setUp(fixer_pkg=fixer_pkg)

if __name__ == "__main__":
    for module in os.listdir(os.path.split(__file__)[0]):
        if module.endswith('.py') and module.startswith('test_'):
            module = os.path.split(module)[1][:-3]
            if module != os.path.split(__file__)[1][:-3]:
                _module = __import__(module)
                support.run_all_tests(_module)
