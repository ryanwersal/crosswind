import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(two_to_three_test_case):
    return two_to_three_test_case("repr")


def test_prefix_preservation(fixer):
    b = """x =   `1 + 2`"""
    a = """x =   repr(1 + 2)"""
    fixer.check(b, a)


def test_simple_1(fixer):
    b = """x = `1 + 2`"""
    a = """x = repr(1 + 2)"""
    fixer.check(b, a)


def test_simple_2(fixer):
    b = """y = `x`"""
    a = """y = repr(x)"""
    fixer.check(b, a)


def test_complex(fixer):
    b = """z = `y`.__repr__()"""
    a = """z = repr(y).__repr__()"""
    fixer.check(b, a)


def test_tuple(fixer):
    b = """x = `1, 2, 3`"""
    a = """x = repr((1, 2, 3))"""
    fixer.check(b, a)


def test_nested(fixer):
    b = """x = `1 + `2``"""
    a = """x = repr(1 + repr(2))"""
    fixer.check(b, a)


def test_nested_tuples(fixer):
    b = """x = `1, 2 + `3, 4``"""
    a = """x = repr((1, 2 + repr((3, 4))))"""
    fixer.check(b, a)
