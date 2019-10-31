import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(two_to_three_test_case):
    return two_to_three_test_case("reload")


def test(fixer):
    b = """reload(a)"""
    a = """import importlib\nimportlib.reload(a)"""
    fixer.check(b, a)


def test_comment(fixer):
    b = """reload( a ) # comment"""
    a = """import importlib\nimportlib.reload( a ) # comment"""
    fixer.check(b, a)

    # PEP 8 comments
    b = """reload( a )  # comment"""
    a = """import importlib\nimportlib.reload( a )  # comment"""
    fixer.check(b, a)


def test_space(fixer):
    b = """reload( a )"""
    a = """import importlib\nimportlib.reload( a )"""
    fixer.check(b, a)

    b = """reload( a)"""
    a = """import importlib\nimportlib.reload( a)"""
    fixer.check(b, a)

    b = """reload(a )"""
    a = """import importlib\nimportlib.reload(a )"""
    fixer.check(b, a)


def test_unchanged(fixer):
    s = """reload(a=1)"""
    fixer.unchanged(s)

    s = """reload(f, g)"""
    fixer.unchanged(s)

    s = """reload(f, *h)"""
    fixer.unchanged(s)

    s = """reload(f, *h, **i)"""
    fixer.unchanged(s)

    s = """reload(f, **i)"""
    fixer.unchanged(s)

    s = """reload(*h, **i)"""
    fixer.unchanged(s)

    s = """reload(*h)"""
    fixer.unchanged(s)

    s = """reload(**i)"""
    fixer.unchanged(s)

    s = """reload()"""
    fixer.unchanged(s)
