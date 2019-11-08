import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(three_to_two_test_case):
    return three_to_two_test_case("reload")


def test_import_removal(fixer):
    b = """import importlib\nimportlib.reload(a)"""
    a = """\nreload(a)"""
    fixer.check(b, a)


def test_comment(fixer):
    b = """import importlib\nimportlib.reload( a ) # comment"""
    a = """\nreload( a ) # comment"""
    fixer.check(b, a)

    # PEP 8 comments
    b = """import importlib\nimportlib.reload( a )  # comment"""
    a = """\nreload( a )  # comment"""
    fixer.check(b, a)


def test_space(fixer):
    b = """import importlib\nimportlib.reload( a )"""
    a = """\nreload( a )"""
    fixer.check(b, a)

    b = """import importlib\nimportlib.reload( a)"""
    a = """\nreload( a)"""
    fixer.check(b, a)

    b = """import importlib\nimportlib.reload(a )"""
    a = """\nreload(a )"""
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
