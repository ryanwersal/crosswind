import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(three_to_two_test_case):
    return three_to_two_test_case("int")


def test_1(fixer):
    b = """x = int(x)"""
    a = """x = long(x)"""
    fixer.check(b, a)


def test_2(fixer):
    b = """y = isinstance(x, int)"""
    a = """y = isinstance(x, long)"""
    fixer.check(b, a)


def test_unchanged(fixer):
    s = """int = True"""
    fixer.unchanged(s)

    s = """s.int = True"""
    fixer.unchanged(s)

    s = """def int(): pass"""
    fixer.unchanged(s)

    s = """class int(): pass"""
    fixer.unchanged(s)

    s = """def f(int): pass"""
    fixer.unchanged(s)

    s = """def f(g, int): pass"""
    fixer.unchanged(s)

    s = """def f(x, int=True): pass"""
    fixer.unchanged(s)


def test_prefix_preservation(fixer):
    b = """x =   int(  x  )"""
    a = """x =   long(  x  )"""
    fixer.check(b, a)


def test_literal_1(fixer):
    b = """5"""
    a = """5L"""
    fixer.check(b, a)


def test_literal_2(fixer):
    b = """a = 12"""
    a = """a = 12L"""
    fixer.check(b, a)


def test_literal_3(fixer):
    b = """0"""
    a = """0L"""
    fixer.check(b, a)


def test_complex_1(fixer):
    b = """5 + 4j"""
    a = """5L + 4j"""
    fixer.check(b, a)


def test_complex_2(fixer):
    b = """35  +  2j"""
    a = """35L  +  2j"""
    fixer.check(b, a)
