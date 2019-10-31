import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(three_to_two_test_case):
    return three_to_two_test_case("str")


def test_str_call(fixer):
    b = """str(x, y, z)"""
    a = """unicode(x, y, z)"""
    fixer.check(b, a)


def test_chr_call_unchanged(fixer):
    u = """chr(a, t, m)"""
    fixer.unchanged(u)


def test_str_literal_1(fixer):
    b = '''"x"'''
    a = '''u"x"'''
    fixer.check(b, a)


def test_str_literal_2(fixer):
    b = """r'x'"""
    a = """ur'x'"""
    fixer.check(b, a)


def test_str_literal_3(fixer):
    b = """R'''x'''"""
    a = """uR'''x'''"""
    fixer.check(b, a)
