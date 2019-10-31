import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(two_to_three_test_case):
    return two_to_three_test_case("standarderror")


def test(fixer):
    b = """x =    StandardError()"""
    a = """x =    Exception()"""
    fixer.check(b, a)

    b = """x = StandardError(a, b, c)"""
    a = """x = Exception(a, b, c)"""
    fixer.check(b, a)

    b = """f(2 + StandardError(a, b, c))"""
    a = """f(2 + Exception(a, b, c))"""
    fixer.check(b, a)
