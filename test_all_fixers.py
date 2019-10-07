#!/usr/bin/env python3.2
"""
Runs all test cases in tests directory named test_*.py
"""

import os.path
import os
import importlib
import crosswind.tests.support as support

tests_package = 'crosswind.tests'

if __name__ == "__main__":
    from sys import exit
    passed = True
    for module in os.listdir(tests_package.replace('.', os.sep)):
        if module.endswith('.py') and module.startswith('test_'):
            module = tests_package + '.' + module[:-3]
            _module = importlib.import_module(module)
            result = support.run_all_tests(_module)
            passed = passed and not result.failures
    if not passed:
       exit(1)
