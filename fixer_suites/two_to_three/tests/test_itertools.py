import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(two_to_three_test_case):
    return two_to_three_test_case("itertools")


def checkall(fixer, before, after):
    # Because we need to check with and without the itertools prefix
    # and on each of the three functions, these loops make it all
    # much easier
    for i in ("itertools.", ""):
        for f in ("map", "filter", "zip"):
            b = before % (i + "i" + f)
            a = after % (f)
            fixer.check(b, a)


def test_0(fixer):
    # A simple example -- test_1 covers exactly the same thing,
    # but it's not quite as clear.
    b = "itertools.izip(a, b)"
    a = "zip(a, b)"
    fixer.check(b, a)


def test_1(fixer):
    b = """%s(f, a)"""
    a = """%s(f, a)"""
    checkall(fixer, b, a)


def test_qualified(fixer):
    b = """itertools.ifilterfalse(a, b)"""
    a = """itertools.filterfalse(a, b)"""
    fixer.check(b, a)

    b = """itertools.izip_longest(a, b)"""
    a = """itertools.zip_longest(a, b)"""
    fixer.check(b, a)


def test_2(fixer):
    b = """ifilterfalse(a, b)"""
    a = """filterfalse(a, b)"""
    fixer.check(b, a)

    b = """izip_longest(a, b)"""
    a = """zip_longest(a, b)"""
    fixer.check(b, a)


def test_space_1(fixer):
    b = """    %s(f, a)"""
    a = """    %s(f, a)"""
    checkall(fixer, b, a)


def test_space_2(fixer):
    b = """    itertools.ifilterfalse(a, b)"""
    a = """    itertools.filterfalse(a, b)"""
    fixer.check(b, a)

    b = """    itertools.izip_longest(a, b)"""
    a = """    itertools.zip_longest(a, b)"""
    fixer.check(b, a)


def test_run_order(fixer):
    fixer.assert_runs_after("map", "zip", "filter")
