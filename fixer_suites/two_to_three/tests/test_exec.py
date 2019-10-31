import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(two_to_three_test_case):
    return two_to_three_test_case("exec")


def test_prefix_preservation(fixer):
    b = """  exec code in ns1,   ns2"""
    a = """  exec(code, ns1,   ns2)"""
    fixer.check(b, a)


def test_basic(fixer):
    b = """exec code"""
    a = """exec(code)"""
    fixer.check(b, a)


def test_with_globals(fixer):
    b = """exec code in ns"""
    a = """exec(code, ns)"""
    fixer.check(b, a)


def test_with_globals_locals(fixer):
    b = """exec code in ns1, ns2"""
    a = """exec(code, ns1, ns2)"""
    fixer.check(b, a)


def test_complex_1(fixer):
    b = """exec (a.b()) in ns"""
    a = """exec((a.b()), ns)"""
    fixer.check(b, a)


def test_complex_2(fixer):
    b = """exec a.b() + c in ns"""
    a = """exec(a.b() + c, ns)"""
    fixer.check(b, a)


# These should not be touched


def test_unchanged_1(fixer):
    s = """exec(code)"""
    fixer.unchanged(s)


def test_unchanged_2(fixer):
    s = """exec (code)"""
    fixer.unchanged(s)


def test_unchanged_3(fixer):
    s = """exec(code, ns)"""
    fixer.unchanged(s)


def test_unchanged_4(fixer):
    s = """exec(code, ns1, ns2)"""
    fixer.unchanged(s)
