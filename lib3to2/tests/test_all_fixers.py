#!/usr/bin/env python2.7
"""Tests that run all fixer modules over an input stream.

This has been broken out into its own test module because of its
running time.
"""

# Python imports
import unittest
import os.path
import os

# Local imports
from lib2to3 import pytree
from lib2to3 import refactor
from lib2to3.tests import support

if __name__ == "__main__":
    for module in os.listdir(os.path.split(__file__)[0]):
        if module.endswith('.py'):
            module = os.path.split(module)[1][:-3]
            if module != os.path.split(__file__)[1][:-3] and \
               module != 'test_fixers':
                _module = __import__(module)
                support.run_all_tests(_module)
