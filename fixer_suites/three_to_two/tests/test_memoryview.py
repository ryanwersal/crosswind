import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(three_to_two_test_case):
    return three_to_two_test_case("memoryview")


def test_simple(fixer):
    b = """x = memoryview(y)"""
    a = """x = buffer(y)"""
    fixer.check(b, a)


def test_slicing(fixer):
    b = """x = memoryview(y)[1:4]"""
    a = """x = buffer(y)[1:4]"""
    fixer.check(b, a)


def test_prefix_preservation(fixer):
    b = """x =       memoryview(  y )[1:4]"""
    a = """x =       buffer(  y )[1:4]"""
    fixer.check(b, a)


def test_nested(fixer):
    b = """x = list(memoryview(y)[1:4])"""
    a = """x = list(buffer(y)[1:4])"""
    fixer.check(b, a)
