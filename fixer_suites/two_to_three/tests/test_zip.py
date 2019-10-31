import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(two_to_three_test_case):
    return two_to_three_test_case("zip")


def check(fixer, b, a):
    fixer.unchanged("from future_builtins import zip; " + b, a)
    fixer.check(b, a)


def test_zip_basic(fixer):
    b = """x = zip()"""
    a = """x = list(zip())"""
    fixer.check(b, a)

    b = """x = zip(a, b, c)"""
    a = """x = list(zip(a, b, c))"""
    fixer.check(b, a)

    b = """x = len(zip(a, b))"""
    a = """x = len(list(zip(a, b)))"""
    fixer.check(b, a)


def test_zip_trailers(fixer):
    b = """x = zip(a, b, c)[0]"""
    a = """x = list(zip(a, b, c))[0]"""
    fixer.check(b, a)

    b = """x = zip(a, b, c)[0][1]"""
    a = """x = list(zip(a, b, c))[0][1]"""
    fixer.check(b, a)


def test_zip_nochange(fixer):
    a = """b.join(zip(a, b))"""
    fixer.unchanged(a)
    a = """(a + foo(5)).join(zip(a, b))"""
    fixer.unchanged(a)
    a = """iter(zip(a, b))"""
    fixer.unchanged(a)
    a = """list(zip(a, b))"""
    fixer.unchanged(a)
    a = """list(zip(a, b))[0]"""
    fixer.unchanged(a)
    a = """set(zip(a, b))"""
    fixer.unchanged(a)
    a = """set(zip(a, b)).pop()"""
    fixer.unchanged(a)
    a = """tuple(zip(a, b))"""
    fixer.unchanged(a)
    a = """any(zip(a, b))"""
    fixer.unchanged(a)
    a = """all(zip(a, b))"""
    fixer.unchanged(a)
    a = """sum(zip(a, b))"""
    fixer.unchanged(a)
    a = """sorted(zip(a, b))"""
    fixer.unchanged(a)
    a = """sorted(zip(a, b), key=blah)"""
    fixer.unchanged(a)
    a = """sorted(zip(a, b), key=blah)[0]"""
    fixer.unchanged(a)
    a = """enumerate(zip(a, b))"""
    fixer.unchanged(a)
    a = """enumerate(zip(a, b), start=1)"""
    fixer.unchanged(a)
    a = """for i in zip(a, b): pass"""
    fixer.unchanged(a)
    a = """[x for x in zip(a, b)]"""
    fixer.unchanged(a)
    a = """(x for x in zip(a, b))"""
    fixer.unchanged(a)


def test_future_builtins(fixer):
    a = "from future_builtins import spam, zip, eggs; zip(a, b)"
    fixer.unchanged(a)

    b = """from future_builtins import spam, eggs; x = zip(a, b)"""
    a = """from future_builtins import spam, eggs; x = list(zip(a, b))"""
    fixer.check(b, a)

    a = "from future_builtins import *; zip(a, b)"
    fixer.unchanged(a)
