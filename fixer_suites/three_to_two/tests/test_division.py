import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(three_to_two_test_case):
    return three_to_two_test_case("division")


def test_one(fixer):
    b = """1/2"""
    a = """from __future__ import division
1/2"""
    fixer.check(b, a)


def test_two(fixer):
    b = """spam/eggs"""
    a = """from __future__ import division
spam/eggs"""
    fixer.check(b, a)


def test_three(fixer):
    b = """lambda a: a(4)/my_foot(your_face)"""
    a = """from __future__ import division
lambda a: a(4)/my_foot(your_face)"""
    fixer.check(b, a)


def test_four(fixer):
    b = """temp(bob)/4"""
    a = """from __future__ import division
temp(bob)/4"""
    fixer.check(b, a)


def test_five(fixer):
    b = """29.4/green()"""
    a = """from __future__ import division
29.4/green()"""
    fixer.check(b, a)
