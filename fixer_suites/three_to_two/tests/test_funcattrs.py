import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(three_to_two_test_case):
    return three_to_two_test_case("funcattrs")


def test_doc_unchanged(fixer):
    b = """whats.up.__doc__"""
    fixer.unchanged(b)


def test_defaults(fixer):
    b = """myFunc.__defaults__"""
    a = """myFunc.func_defaults"""
    fixer.check(b, a)


def test_closure(fixer):
    b = """fore.__closure__"""
    a = """fore.func_closure"""
    fixer.check(b, a)


def test_globals(fixer):
    b = """funkFunc.__globals__"""
    a = """funkFunc.func_globals"""
    fixer.check(b, a)


def test_dict_unchanged(fixer):
    b = """tricky.__dict__"""
    fixer.unchanged(b)


def test_name_unchanged(fixer):
    b = """sayMy.__name__"""
    fixer.unchanged(b)
