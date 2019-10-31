import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(three_to_two_test_case):
    return three_to_two_test_case("fullargspec")


def test_import(fixer):
    b = "from inspect import blah, blah, getfullargspec, blah, blah"
    a = "from inspect import blah, blah, getargspec, blah, blah"
    fixer.warns(b, a, "some of the values returned by getfullargspec are not valid in Python 2 and have no equivalent.")


def test_usage(fixer):
    b = "argspec = inspect.getfullargspec(func)"
    a = "argspec = inspect.getargspec(func)"
    fixer.warns(b, a, "some of the values returned by getfullargspec are not valid in Python 2 and have no equivalent.")
