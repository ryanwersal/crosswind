#!/usr/bin/env python3.1
"""
Runs all test cases in tests directory named test_*.py
"""

import os.path
import os
import importlib
import lib3to2.tests.support as support

tests_package = 'lib3to2.tests'

if __name__ == "__main__":
    for module in os.listdir(tests_package.replace('.', os.sep)):
        if module.endswith('.py') and module.startswith('test_'):
            module = tests_package + '.' + module[:-3]
            _module = importlib.import_module(module)
            support.run_all_tests(_module)
