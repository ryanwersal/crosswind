import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(two_to_three_test_case):
    return two_to_three_test_case("buffer")


def test_buffer(fixer):
    b = """x = buffer(y)"""
    a = """x = memoryview(y)"""
    fixer.check(b, a)


def test_slicing(fixer):
    b = """buffer(y)[4:5]"""
    a = """memoryview(y)[4:5]"""
    fixer.check(b, a)
