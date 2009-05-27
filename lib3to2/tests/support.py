"""Support code for test_*.py files"""

# Python imports
import unittest
import sys
import os
import os.path
import re
from itertools import chain
from operator import itemgetter
from textwrap import dedent

import refactor
from lib2to3 import pygram, pytree, fixer_util
from lib2to3.pgen2 import driver

test_dir = os.path.dirname(__file__)
proj_dir = os.path.normpath(os.path.join(test_dir, ".."))
grammar_path = os.path.join(test_dir, "..", "Grammar.txt")
grammar = driver.load_grammar(grammar_path)
driver = driver.Driver(grammar, convert=pytree.convert)

def parse_string(string):
    return driver.parse_string(reformat(string), debug=True)

def run_all_tests(test_mod=None, tests=None):
    if tests is None:
        tests = unittest.TestLoader().loadTestsFromModule(test_mod)
    unittest.TextTestRunner(verbosity=2).run(tests)

def reformat(string):
    return dedent(string) + u"\n\n"

def get_refactorer(fixers=None, options=None):
    """
    A convenience function for creating a RefactoringTool for tests.

    fixers is a list of fixers for the RefactoringTool to use. By default
    "lib2to3.fixes.*" is used. options is an optional dictionary of options to
    be passed to the RefactoringTool.
    """
    if fixers is not None:
        fixers = ["lib3to2.fixes.fix_" + fix for fix in fixers]
    else:
        fixers = refactor.get_fixers_from_package("lib3to2.fixes")
    options = options or {}
    return refactor.RefactoringTool(fixers, options, explicit=True)

def all_project_files():
    for dirpath, dirnames, filenames in os.walk(proj_dir):
        for filename in filenames:
            if filename.endswith(".py") and filename.startswith("test_"):
                yield os.path.join(dirpath, filename)

TestCase = unittest.TestCase
class FixerTestCase(TestCase):
    def setUp(self, fix_list=None):
        if fix_list is None:
            fix_list = [self.fixer]
        options = {"print_function" : False}
        self.refactor = get_refactorer(fix_list, options)
        self.fixer_log = []
        self.filename = u"<string>"

        for fixer in chain(self.refactor.pre_order,
                           self.refactor.post_order):
            fixer.log = self.fixer_log

    def _check(self, before, after):
        before = reformat(before)
        after = reformat(after)
        tree = self.refactor.refactor_string(before, self.filename)
        self.failUnlessEqual(after, unicode(tree))
        return tree

    def check(self, before, after, ignore_warnings=False):
        tree = self._check(before, after)
        self.failUnless(tree.was_changed)
        if not ignore_warnings:
            self.failUnlessEqual(self.fixer_log, [])

    def warns(self, before, after, message, unchanged=False):
        tree = self._check(before, after)
        self.failUnless(message in "".join(self.fixer_log))
        if not unchanged:
            self.failUnless(tree.was_changed)

    def warns_unchanged(self, before, message):
        self.warns(before, before, message, unchanged=True)

    def unchanged(self, before, ignore_warnings=False):
        self._check(before, before)
        if not ignore_warnings:
            self.failUnlessEqual(self.fixer_log, [])

    def assert_runs_after(self, *names):
        fixes = [self.fixer]
        fixes.extend(names)
        options = {"print_function" : False}
        r = get_refactorer(fixes, options)
        (pre, post) = r.get_fixers()
        n = "fix_" + self.fixer
        if post and post[-1].__class__.__module__.endswith(n):
            # We're the last fixer to run
            return
        if pre and pre[-1].__class__.__module__.endswith(n) and not post:
            # We're the last in pre and post is empty
            return
        self.fail("Fixer run order (%s) is incorrect; %s should be last."\
               %(", ".join([x.__class__.__module__ for x in (pre+post)]), n))
