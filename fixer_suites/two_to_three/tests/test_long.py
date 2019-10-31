import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(two_to_three_test_case):
    return two_to_three_test_case("long")


def test_1(fixer):
    b = """x = long(x)"""
    a = """x = int(x)"""
    fixer.check(b, a)


def test_2(fixer):
    b = """y = isinstance(x, long)"""
    a = """y = isinstance(x, int)"""
    fixer.check(b, a)


def test_3(fixer):
    b = """z = type(x) in (int, long)"""
    a = """z = type(x) in (int, int)"""
    fixer.check(b, a)


def test_unchanged(fixer):
    s = """long = True"""
    fixer.unchanged(s)

    s = """s.long = True"""
    fixer.unchanged(s)

    s = """def long(): pass"""
    fixer.unchanged(s)

    s = """class long(): pass"""
    fixer.unchanged(s)

    s = """def f(long): pass"""
    fixer.unchanged(s)

    s = """def f(g, long): pass"""
    fixer.unchanged(s)

    s = """def f(x, long=True): pass"""
    fixer.unchanged(s)


def test_prefix_preservation(fixer):
    b = """x =   long(  x  )"""
    a = """x =   int(  x  )"""
    fixer.check(b, a)
