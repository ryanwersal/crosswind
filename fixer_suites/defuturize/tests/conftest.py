import pytest

from crosswind.tests.test_fixtures import fixer_test_case_fixture  # pylint: disable=unused-import


@pytest.fixture(name="defuturize_test_case")
def defuturize_fixture(fixer_test_case):
    """
    Fixture to fill in fixer_pkg of fixer_test_case fixture.
    """

    def __init_fixer_suite_test_case(fixer_name, fix_list=None, options=None):
        return fixer_test_case(fixer_name, "fixer_suites.defuturize", fix_list=fix_list, options=options)

    return __init_fixer_suite_test_case
