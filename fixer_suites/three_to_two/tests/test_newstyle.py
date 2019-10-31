import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(three_to_two_test_case):
    return three_to_two_test_case("newstyle")


def test_oneline(fixer):

    b = """class Foo: pass"""
    a = """class Foo(object): pass"""
    fixer.check(b, a)


def test_suite(fixer):

    b = """
    class Foo():
        do_stuff()"""
    a = """
    class Foo(object):
        do_stuff()"""
    fixer.check(b, a)
