import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(two_to_three_test_case):
    return two_to_three_test_case("isinstance")


def test_remove_multiple_items(fixer):
    b = """isinstance(x, (int, int, int))"""
    a = """isinstance(x, int)"""
    fixer.check(b, a)

    b = """isinstance(x, (int, float, int, int, float))"""
    a = """isinstance(x, (int, float))"""
    fixer.check(b, a)

    b = """isinstance(x, (int, float, int, int, float, str))"""
    a = """isinstance(x, (int, float, str))"""
    fixer.check(b, a)

    b = """isinstance(foo() + bar(), (x(), y(), x(), int, int))"""
    a = """isinstance(foo() + bar(), (x(), y(), x(), int))"""
    fixer.check(b, a)


def test_prefix_preservation(fixer):
    b = """if    isinstance(  foo(), (  bar, bar, baz )) : pass"""
    a = """if    isinstance(  foo(), (  bar, baz )) : pass"""
    fixer.check(b, a)


def test_unchanged(fixer):
    fixer.unchanged("isinstance(x, (str, int))")
