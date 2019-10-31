"""Support code for test_*.py files"""
# Author: Collin Winter

import os
import os.path
from itertools import chain
from textwrap import dedent

import pytest

from crosswind import pygram, pytree, refactor
from crosswind.pgen2 import driver as pgen2_driver


test_dir = os.path.dirname(__file__)
proj_dir = os.path.normpath(os.path.join(test_dir, ".."))
grammar_path = pygram.GRAMMAR_FILE
grammar = pgen2_driver.load_grammar(grammar_path)
grammar_no_print_statement = pgen2_driver.load_grammar(grammar_path)
del grammar_no_print_statement.keywords["print"]
driver = pgen2_driver.Driver(grammar, convert=pytree.convert)
driver_no_print_statement = pgen2_driver.Driver(grammar_no_print_statement, convert=pytree.convert)


def parse_string(string):
    return driver.parse_string(reformat(string), debug=True)


def reformat(string):
    return dedent(string) + "\n\n"


def get_refactorer(fixer_pkg="fixer_suites.two_to_three", fixers=None, options=None):
    """
    A convenience function for creating a RefactoringTool for tests.

    fixers is a list of fixers for the RefactoringTool to use. By default
    "fixer_suites.two_to_three.fixes.*" is used. options is an optional dictionary of options to
    be passed to the RefactoringTool.
    """
    if fixers is not None:
        fixers = [fixer_pkg + ".fixes.fix_" + fix for fix in fixers]
    else:
        fixers = refactor.get_fixers_from_package(fixer_pkg + ".fixes")
    options = options or {}
    return refactor.RefactoringTool(fixers, options, explicit=True)


def all_project_files():
    for dirpath, dirnames, filenames in os.walk(proj_dir):
        for filename in filenames:
            if filename.endswith(".py"):
                yield os.path.join(dirpath, filename)


class FixerTestCase:
    fixer = None

    # Other test cases can subclass this class and replace "fixer_pkg" with
    # their own.
    def setUp(self, fix_list=None, fixer_pkg="fixer_suites.two_to_three", options=None):
        if fix_list is None:
            if self.fixer is None:
                raise "'fixer' must be specified for each FixerTestCase"

            fix_list = [self.fixer]
        self.refactor = get_refactorer(fixer_pkg, fix_list, options)
        self.fixer_log = []
        self.filename = "<string>"

        for fixer in chain(self.refactor.pre_order, self.refactor.post_order):
            fixer.log = self.fixer_log

    def _check(self, before, after):
        before = reformat(before)
        after = reformat(after)
        tree = self.refactor.refactor_string(before, self.filename)
        assert after == str(tree)
        return tree

    def check(self, before, after, ignore_warnings=False):
        tree = self._check(before, after)
        assert tree.was_changed
        if not ignore_warnings:
            assert self.fixer_log == []

    def warns(self, before, after, message, unchanged=False):
        tree = self._check(before, after)
        assert message in "".join(self.fixer_log)
        if not unchanged:
            assert tree.was_changed

    def warns_unchanged(self, before, message):
        self.warns(before, before, message, unchanged=True)

    def unchanged(self, before, ignore_warnings=False):
        self._check(before, before)
        if not ignore_warnings:
            assert self.fixer_log == []

    def assert_runs_after(self, *names):
        fixes = [self.fixer]
        fixes.extend(names)
        r = get_refactorer("fixer_suites.two_to_three", fixes)
        (pre, post) = r.get_fixers()
        n = "fix_" + self.fixer
        if post and post[-1].__class__.__module__.endswith(n):
            # We're the last fixer to run
            return
        if pre and pre[-1].__class__.__module__.endswith(n) and not post:
            # We're the last in pre and post is empty
            return
        pytest.fail(
            "Fixer run order (%s) is incorrect; %s should be last."
            % (", ".join([x.__class__.__module__ for x in pre + post]), n)
        )
