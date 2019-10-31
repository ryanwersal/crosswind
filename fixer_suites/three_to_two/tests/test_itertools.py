import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(three_to_two_test_case):
    return three_to_two_test_case("itertools")


def test_map(fixer):
    b = """map(a, b)"""
    a = """from itertools import imap\nimap(a, b)"""
    fixer.check(b, a)


def test_unchanged_nobuiltin(fixer):
    s = """obj.filter(a, b)"""
    fixer.unchanged(s)

    s = """
    def map():
        pass
    """
    fixer.unchanged(s)


def test_filter(fixer):
    b = "a =    filter( a,  b)"
    a = "from itertools import ifilter\na =    ifilter( a,  b)"
    fixer.check(b, a)


def test_zip(fixer):
    b = """for key, val in zip(a, b):\n\tdct[key] = val"""
    a = """from itertools import izip\nfor key, val in izip(a, b):\n\tdct[key] = val"""
    fixer.check(b, a)


def test_filterfalse(fixer):
    b = """from itertools import function, filterfalse, other_function"""
    a = """from itertools import function, ifilterfalse, other_function"""
    fixer.check(b, a)

    b = """filterfalse(a, b)"""
    a = """ifilterfalse(a, b)"""
    fixer.check(b, a)
