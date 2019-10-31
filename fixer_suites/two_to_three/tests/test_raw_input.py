import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(two_to_three_test_case):
    return two_to_three_test_case("raw_input")


def test_prefix_preservation(fixer):
    b = """x =    raw_input(   )"""
    a = """x =    input(   )"""
    fixer.check(b, a)

    b = """x = raw_input(   ''   )"""
    a = """x = input(   ''   )"""
    fixer.check(b, a)


def test_1(fixer):
    b = """x = raw_input()"""
    a = """x = input()"""
    fixer.check(b, a)


def test_2(fixer):
    b = """x = raw_input('')"""
    a = """x = input('')"""
    fixer.check(b, a)


def test_3(fixer):
    b = """x = raw_input('prompt')"""
    a = """x = input('prompt')"""
    fixer.check(b, a)


def test_4(fixer):
    b = """x = raw_input(foo(a) + 6)"""
    a = """x = input(foo(a) + 6)"""
    fixer.check(b, a)


def test_5(fixer):
    b = """x = raw_input(invite).split()"""
    a = """x = input(invite).split()"""
    fixer.check(b, a)


def test_6(fixer):
    b = """x = raw_input(invite) . split ()"""
    a = """x = input(invite) . split ()"""
    fixer.check(b, a)


def test_8(fixer):
    b = "x = int(raw_input())"
    a = "x = int(input())"
    fixer.check(b, a)
