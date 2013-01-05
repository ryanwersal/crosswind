#!/usr/bin/env python3.1
"""
Runs all test cases in tests directory named test_*.py
"""

import os.path
import os
import importlib
import lib3to2.tests.support as support

tests_directory = 'lib3to2/tests'  # Relative path to test directory.

if __name__ == "__main__":
    for module in os.listdir(tests_directory):
        if module.endswith('.py') and module.startswith('test_'):
            module = os.path.join(tests_directory, module[:-3])
            module = module.replace(os.sep, '.')
            _module = importlib.import_module(module)
            support.run_all_tests(_module)
