import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(two_to_three_test_case):
    return two_to_three_test_case("input")


def test_prefix_preservation(fixer):
    b = """x =   input(   )"""
    a = """x =   eval(input(   ))"""
    fixer.check(b, a)

    b = """x = input(   ''   )"""
    a = """x = eval(input(   ''   ))"""
    fixer.check(b, a)


def test_trailing_comment(fixer):
    b = """x = input()  #  foo"""
    a = """x = eval(input())  #  foo"""
    fixer.check(b, a)


def test_idempotency(fixer):
    s = """x = eval(input())"""
    fixer.unchanged(s)

    s = """x = eval(input(''))"""
    fixer.unchanged(s)

    s = """x = eval(input(foo(5) + 9))"""
    fixer.unchanged(s)


def test_1(fixer):
    b = """x = input()"""
    a = """x = eval(input())"""
    fixer.check(b, a)


def test_2(fixer):
    b = """x = input('')"""
    a = """x = eval(input(''))"""
    fixer.check(b, a)


def test_3(fixer):
    b = """x = input('prompt')"""
    a = """x = eval(input('prompt'))"""
    fixer.check(b, a)


def test_4(fixer):
    b = """x = input(foo(5) + 9)"""
    a = """x = eval(input(foo(5) + 9))"""
    fixer.check(b, a)
