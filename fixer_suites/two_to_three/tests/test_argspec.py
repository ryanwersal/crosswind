import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(two_to_three_test_case):
    return two_to_three_test_case("argspec")


def test_import(fixer):
    b = "from inspect import blah, blah, getargspec, blah, blah"
    a = "from inspect import blah, blah, getfullargspec, blah, blah"
    fixer.check(b, a, "some of the values returned by getargspec are not valid in Python 2 and have no equivalent.")


def test_usage(fixer):
    b = "argspec = inspect.getargspec(func)"
    a = "argspec = inspect.getfullargspec(func)"
    fixer.check(b, a, "some of the values returned by getargspec are not valid in Python 2 and have no equivalent.")
