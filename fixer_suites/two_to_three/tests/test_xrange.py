import pytest

from crosswind import fixer_util


@pytest.fixture(name="fixer")
def fixer_fixture(two_to_three_test_case):
    return two_to_three_test_case("xrange")


def test_prefix_preservation(fixer):
    b = """x =    xrange(  10  )"""
    a = """x =    range(  10  )"""
    fixer.check(b, a)

    b = """x = xrange(  1  ,  10   )"""
    a = """x = range(  1  ,  10   )"""
    fixer.check(b, a)

    b = """x = xrange(  0  ,  10 ,  2 )"""
    a = """x = range(  0  ,  10 ,  2 )"""
    fixer.check(b, a)


def test_single_arg(fixer):
    b = """x = xrange(10)"""
    a = """x = range(10)"""
    fixer.check(b, a)


def test_two_args(fixer):
    b = """x = xrange(1, 10)"""
    a = """x = range(1, 10)"""
    fixer.check(b, a)


def test_three_args(fixer):
    b = """x = xrange(0, 10, 2)"""
    a = """x = range(0, 10, 2)"""
    fixer.check(b, a)


def test_wrap_in_list(fixer):
    b = """x = range(10, 3, 9)"""
    a = """x = list(range(10, 3, 9))"""
    fixer.check(b, a)

    b = """x = foo(range(10, 3, 9))"""
    a = """x = foo(list(range(10, 3, 9)))"""
    fixer.check(b, a)

    b = """x = range(10, 3, 9) + [4]"""
    a = """x = list(range(10, 3, 9)) + [4]"""
    fixer.check(b, a)

    b = """x = range(10)[::-1]"""
    a = """x = list(range(10))[::-1]"""
    fixer.check(b, a)

    b = """x = range(10)  [3]"""
    a = """x = list(range(10))  [3]"""
    fixer.check(b, a)


def test_xrange_in_for(fixer):
    b = """for i in xrange(10):\n    j=i"""
    a = """for i in range(10):\n    j=i"""
    fixer.check(b, a)

    b = """[i for i in xrange(10)]"""
    a = """[i for i in range(10)]"""
    fixer.check(b, a)


def test_range_in_for(fixer):
    fixer.unchanged("for i in range(10): pass")
    fixer.unchanged("[i for i in range(10)]")


def test_in_contains_test(fixer):
    fixer.unchanged("x in range(10, 3, 9)")


def test_in_consuming_context(fixer):
    for call in fixer_util.consuming_calls:
        fixer.unchanged("a = %s(range(10))" % call)
