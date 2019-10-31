import pytest

from crosswind import pygram
from crosswind.tests.test_fixtures import fixer_test_case_fixture  # pylint: disable=unused-import


@pytest.fixture(name="three_to_two_test_case")
def three_to_two_fixture(fixer_test_case):
    """
    Fixture to fill in fixer_pkg of fixer_test_case fixture.
    """

    def __init_fixer_suite_test_case(fixer_name, fix_list=None, options=None):
        test_case = fixer_test_case(fixer_name, "fixer_suites.three_to_two", fix_list=fix_list, options=options)
        test_case.refactor.driver.grammar = pygram.python_grammar_no_print_statement
        return test_case

    return __init_fixer_suite_test_case
