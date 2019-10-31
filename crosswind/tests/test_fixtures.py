import pytest

from .support import FixerTestCase


@pytest.fixture(name="fixer_test_case")
def fixer_test_case_fixture():
    """
    Fixture that returns a factory function to create a properly configured
    FixerTestCase.
    """

    def __init_fixer_suite_test_case(fixer_name, fixer_pkg, fix_list=None, options=None):
        test_case = FixerTestCase()
        test_case.fixer = fixer_name
        test_case.setUp(fix_list=fix_list, fixer_pkg=fixer_pkg, options=options)
        return test_case

    return __init_fixer_suite_test_case
