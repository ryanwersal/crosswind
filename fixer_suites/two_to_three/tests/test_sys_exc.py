import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(two_to_three_test_case):
    return two_to_three_test_case("sys_exc")


def test_0(fixer):
    b = "sys.exc_type"
    a = "sys.exc_info()[0]"
    fixer.check(b, a)


def test_1(fixer):
    b = "sys.exc_value"
    a = "sys.exc_info()[1]"
    fixer.check(b, a)


def test_2(fixer):
    b = "sys.exc_traceback"
    a = "sys.exc_info()[2]"
    fixer.check(b, a)


def test_3(fixer):
    b = "sys.exc_type # Foo"
    a = "sys.exc_info()[0] # Foo"
    fixer.check(b, a)


def test_4(fixer):
    b = "sys.  exc_type"
    a = "sys.  exc_info()[0]"
    fixer.check(b, a)


def test_5(fixer):
    b = "sys  .exc_type"
    a = "sys  .exc_info()[0]"
    fixer.check(b, a)
