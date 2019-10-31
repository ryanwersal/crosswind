import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(two_to_three_test_case):
    return two_to_three_test_case("paren")


def test_0(fixer):
    b = """[i for i in 1, 2 ]"""
    a = """[i for i in (1, 2) ]"""
    fixer.check(b, a)


def test_1(fixer):
    b = """[i for i in 1, 2, ]"""
    a = """[i for i in (1, 2,) ]"""
    fixer.check(b, a)


def test_2(fixer):
    b = """[i for i  in     1, 2 ]"""
    a = """[i for i  in     (1, 2) ]"""
    fixer.check(b, a)


def test_3(fixer):
    b = """[i for i in 1, 2 if i]"""
    a = """[i for i in (1, 2) if i]"""
    fixer.check(b, a)


def test_4(fixer):
    b = """[i for i in 1,    2    ]"""
    a = """[i for i in (1,    2)    ]"""
    fixer.check(b, a)


def test_5(fixer):
    b = """(i for i in 1, 2)"""
    a = """(i for i in (1, 2))"""
    fixer.check(b, a)


def test_6(fixer):
    b = """(i for i in 1   ,2   if i)"""
    a = """(i for i in (1   ,2)   if i)"""
    fixer.check(b, a)


def test_unchanged_0(fixer):
    s = """[i for i in (1, 2)]"""
    fixer.unchanged(s)


def test_unchanged_1(fixer):
    s = """[i for i in foo()]"""
    fixer.unchanged(s)


def test_unchanged_2(fixer):
    s = """[i for i in (1, 2) if nothing]"""
    fixer.unchanged(s)


def test_unchanged_3(fixer):
    s = """(i for i in (1, 2))"""
    fixer.unchanged(s)


def test_unchanged_4(fixer):
    s = """[i for i in m]"""
    fixer.unchanged(s)
