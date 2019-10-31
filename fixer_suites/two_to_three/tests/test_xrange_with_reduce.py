import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(two_to_three_test_case):
    return two_to_three_test_case("", fix_list=["xrange", "reduce"])


def test_double_transform(fixer):
    b = """reduce(x, xrange(5))"""
    a = """from functools import reduce
reduce(x, range(5))"""
    fixer.check(b, a)
