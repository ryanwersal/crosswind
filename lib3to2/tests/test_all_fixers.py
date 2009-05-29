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
        if fix_list is None:
            fix_list = [self.fixer]
        options = {"print_function" : False}
        self.refactor = support.get_refactorer(fixer_pkg=fixer_pkg, fixers=fix_list, options=options)
        self.fixer_log = []
        self.filename = u"<string>"

        for fixer in chain(self.refactor.pre_order,
                           self.refactor.post_order):
            fixer.log = self.fixer_log

if __name__ == "__main__":
    for module in os.listdir(os.path.split(__file__)[0]):
        if module.endswith('.py'):
            module = os.path.split(module)[1][:-3]
            if module != os.path.split(__file__)[1][:-3] and \
               module != 'test_fixers':
                _module = __import__(module)
                support.run_all_tests(_module)
