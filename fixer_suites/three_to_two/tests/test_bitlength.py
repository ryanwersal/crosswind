import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(three_to_two_test_case):
    return three_to_two_test_case("bitlength")


def test_fixed(fixer):
    b = """a = something.bit_length()"""
    a = """a = (len(bin(something)) - 2)"""
    fixer.check(b, a, ignore_warnings=True)


def test_unfixed(fixer):
    s = """a = bit_length(fire)"""
    fixer.unchanged(s)

    s = """a = s.bit_length('some_arg')"""
    fixer.unchanged(s)
