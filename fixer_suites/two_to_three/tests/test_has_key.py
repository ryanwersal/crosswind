import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(two_to_three_test_case):
    return two_to_three_test_case("has_key")


def test_1(fixer):
    b = """x = d.has_key("x") or d.has_key("y")"""
    a = """x = "x" in d or "y" in d"""
    fixer.check(b, a)


def test_2(fixer):
    b = """x = a.b.c.d.has_key("x") ** 3"""
    a = """x = ("x" in a.b.c.d) ** 3"""
    fixer.check(b, a)


def test_3(fixer):
    b = """x = a.b.has_key(1 + 2).__repr__()"""
    a = """x = (1 + 2 in a.b).__repr__()"""
    fixer.check(b, a)


def test_4(fixer):
    b = """x = a.b.has_key(1 + 2).__repr__() ** -3 ** 4"""
    a = """x = (1 + 2 in a.b).__repr__() ** -3 ** 4"""
    fixer.check(b, a)


def test_5(fixer):
    b = """x = a.has_key(f or g)"""
    a = """x = (f or g) in a"""
    fixer.check(b, a)


def test_6(fixer):
    b = """x = a + b.has_key(c)"""
    a = """x = a + (c in b)"""
    fixer.check(b, a)


def test_7(fixer):
    b = """x = a.has_key(lambda: 12)"""
    a = """x = (lambda: 12) in a"""
    fixer.check(b, a)


def test_8(fixer):
    b = """x = a.has_key(a for a in b)"""
    a = """x = (a for a in b) in a"""
    fixer.check(b, a)


def test_9(fixer):
    b = """if not a.has_key(b): pass"""
    a = """if b not in a: pass"""
    fixer.check(b, a)


def test_10(fixer):
    b = """if not a.has_key(b).__repr__(): pass"""
    a = """if not (b in a).__repr__(): pass"""
    fixer.check(b, a)


def test_11(fixer):
    b = """if not a.has_key(b) ** 2: pass"""
    a = """if not (b in a) ** 2: pass"""
    fixer.check(b, a)
