import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(three_to_two_test_case):
    return three_to_two_test_case("input")


def test_prefix_preservation(fixer):
    b = """x =    input(   )"""
    a = """x =    raw_input(   )"""
    fixer.check(b, a)

    b = """x = input(   ''   )"""
    a = """x = raw_input(   ''   )"""
    fixer.check(b, a)


def test_1(fixer):
    b = """x = input()"""
    a = """x = raw_input()"""
    fixer.check(b, a)


def test_2(fixer):
    b = """x = input('a')"""
    a = """x = raw_input('a')"""
    fixer.check(b, a)


def test_3(fixer):
    b = """x = input('prompt')"""
    a = """x = raw_input('prompt')"""
    fixer.check(b, a)


def test_4(fixer):
    b = """x = input(foo(a) + 6)"""
    a = """x = raw_input(foo(a) + 6)"""
    fixer.check(b, a)


def test_5(fixer):
    b = """x = input(invite).split()"""
    a = """x = raw_input(invite).split()"""
    fixer.check(b, a)


def test_6(fixer):
    b = """x = input(invite) . split ()"""
    a = """x = raw_input(invite) . split ()"""
    fixer.check(b, a)


def test_7(fixer):
    b = "x = int(input())"
    a = "x = int(raw_input())"
    fixer.check(b, a)
