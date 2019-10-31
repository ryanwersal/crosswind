import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(three_to_two_test_case):
    return three_to_two_test_case("except")


def test_prefix_preservation(fixer):
    a = """
        try:
            pass
        except (RuntimeError, ImportError),    e:
            pass"""
    b = """
        try:
            pass
        except (RuntimeError, ImportError) as    e:
            pass"""
    fixer.check(b, a)


def test_simple(fixer):
    a = """
        try:
            pass
        except Foo, e:
            pass"""
    b = """
        try:
            pass
        except Foo as e:
            pass"""
    fixer.check(b, a)
