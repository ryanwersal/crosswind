#!/usr/bin/env python3.1
"""Tests that run all fixer modules over an input stream.

This is a duplicate of lib2to3.tests.test_all_fixers.py
"""

import support

# Python imports
import unittest

# Local imports
from lib2to3 import pytree
from lib3to2 import refactor

class Test_all(support.TestCase):
    def setUp(self):
        options = {"print_function" : False}
        fixers = ['input', 'range']
        self.refactor = support.get_refactorer(fixers=fixers, options=options)

    def test_all_project_files(self):
        for filepath in support.all_project_files():
            print("Fixing %s..." % filepath)
            self.refactor.refactor_file(filepath)


if __name__ == "__main__":
    import __main__
    support.run_all_tests(__main__)
