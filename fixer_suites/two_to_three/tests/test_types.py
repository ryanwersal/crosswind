import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(two_to_three_test_case):
    return two_to_three_test_case("types")


def test_basic_types_convert(fixer):
    b = """types.StringType"""
    a = """bytes"""
    fixer.check(b, a)

    b = """types.DictType"""
    a = """dict"""
    fixer.check(b, a)

    b = """types . IntType"""
    a = """int"""
    fixer.check(b, a)

    b = """types.ListType"""
    a = """list"""
    fixer.check(b, a)

    b = """types.LongType"""
    a = """int"""
    fixer.check(b, a)

    b = """types.NoneType"""
    a = """type(None)"""
    fixer.check(b, a)

    b = "types.StringTypes"
    a = "(str,)"
    fixer.check(b, a)
