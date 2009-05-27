#!/usr/bin/env python2.6
"""Tests that run all fixer modules over an input stream.

This has been broken out into its own test module because of its
running time.
"""

# Python imports
import unittest
import os.path

# Local imports
from lib2to3 import pytree
from lib2to3 import refactor
import support

class Test_all(support.TestCase):
    def setUp(self):
        options = {"print_function" : False}
        self.refactor = support.get_refactorer(options=options)

    def test_all_project_files(self):
        for filepath in support.all_project_files():
            print "Fixing %s..." % filepath
            self.refactor.refactor_file(filepath)


if __name__ == "__main__":
    test_mods = []
    for module in support.all_project_files():
        module = os.path.split(module)[1].strip('.py')
        if module != os.path.split(__file__)[1].strip('.py') and \
           module != 'test_fixers':
            _module = __import__(module)
            support.run_all_tests(_module)
