"""Support code for test_*.py files"""

from crosswind import pygram
from crosswind.tests import support


class crosswindFixerTestCase(support.FixerTestCase):
    # From crosswind.tests.test_all_fixers (moved without changes).
    def setUp(self, fix_list=None, fixer_pkg="fixer_suites.three_to_two", options=None):
        super(crosswindFixerTestCase, self).setUp(fix_list=fix_list, fixer_pkg=fixer_pkg, options=options)
        self.refactor.driver.grammar = pygram.python_grammar_no_print_statement
