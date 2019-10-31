import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(three_to_two_test_case):
    return three_to_two_test_case("range")


def test_notbuiltin_list(fixer):
    b = "x.list(range(10))"
    a = "x.list(xrange(10))"
    fixer.check(b, a)


def test_prefix_preservation(fixer):
    b = """x =    range(  10  )"""
    a = """x =    xrange(  10  )"""
    fixer.check(b, a)

    b = """x = range(  1  ,  10   )"""
    a = """x = xrange(  1  ,  10   )"""
    fixer.check(b, a)

    b = """x = range(  0  ,  10 ,  2 )"""
    a = """x = xrange(  0  ,  10 ,  2 )"""
    fixer.check(b, a)


def test_single_arg(fixer):
    b = """x = range(10)"""
    a = """x = xrange(10)"""
    fixer.check(b, a)


def test_two_args(fixer):
    b = """x = range(1, 10)"""
    a = """x = xrange(1, 10)"""
    fixer.check(b, a)


def test_three_args(fixer):
    b = """x = range(0, 10, 2)"""
    a = """x = xrange(0, 10, 2)"""
    fixer.check(b, a)


def test_wrapped_in_list(fixer):
    b = """x = list(range(10, 3, 9))"""
    a = """x = range(10, 3, 9)"""
    fixer.check(b, a)

    b = """x = foo(list(range(10, 3, 9)))"""
    a = """x = foo(range(10, 3, 9))"""
    fixer.check(b, a)

    b = """x = list(range(10, 3, 9)) + [4]"""
    a = """x = range(10, 3, 9) + [4]"""
    fixer.check(b, a)

    b = """x = list(range(10))[::-1]"""
    a = """x = range(10)[::-1]"""
    fixer.check(b, a)

    b = """x = list(range(10))  [3]"""
    a = """x = range(10)  [3]"""
    fixer.check(b, a)


def test_range_in_for(fixer):
    b = """for i in range(10):\n    j=i"""
    a = """for i in xrange(10):\n    j=i"""
    fixer.check(b, a)

    b = """[i for i in range(10)]"""
    a = """[i for i in xrange(10)]"""
    fixer.check(b, a)
