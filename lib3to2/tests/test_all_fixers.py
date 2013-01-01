#!/usr/bin/env python3.1
"""
Runs all tests in the same directory named test_*.py
"""

import os.path
import os

from lib2to3 import pygram

import lib2to3_support as support
from lib2to3_fixertestcase import FixerTestCase


class lib3to2FixerTestCase(FixerTestCase):
    def setUp(self, fix_list=None, fixer_pkg="lib3to2"):
        super(lib3to2FixerTestCase, self).setUp(fixer_pkg=fixer_pkg)
        self.refactor.driver.grammar = pygram.python_grammar_no_print_statement


if __name__ == "__main__":
    import sys
    repo_path = os.path.join(os.path.dirname(__file__), '../../')
    sys.path.insert(0, repo_path)

    for module in os.listdir(os.path.dirname(os.path.abspath(__file__))):
        if module.endswith('.py') and module.startswith('test_'):
            module = os.path.split(module)[1][:-3]
            if module != os.path.split(__file__)[1][:-3]:
                _module = __import__(module)
                support.run_all_tests(_module)
