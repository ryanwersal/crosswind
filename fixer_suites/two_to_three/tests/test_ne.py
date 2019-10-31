import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(two_to_three_test_case):
    return two_to_three_test_case("ne")


def test_basic(fixer):
    b = """if x <> y:
        pass"""

    a = """if x != y:
        pass"""
    fixer.check(b, a)


def test_no_spaces(fixer):
    b = """if x<>y:
        pass"""

    a = """if x!=y:
        pass"""
    fixer.check(b, a)


def test_chained(fixer):
    b = """if x<>y<>z:
        pass"""

    a = """if x!=y!=z:
        pass"""
    fixer.check(b, a)
