import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(two_to_three_test_case):
    return two_to_three_test_case("basestring")


def test_basestring(fixer):
    b = """isinstance(x, basestring)"""
    a = """isinstance(x, str)"""
    fixer.check(b, a)


def test_isinstance_basestring_tuple(fixer):
    b = "isinstance(x, (basestring, dict))"
    a = "isinstance(x, (str, dict))"
    fixer.check(b, a)

    b = "isinstance(x, (dict, basestring))"
    a = "isinstance(x, (dict, str))"
    fixer.check(b, a)


def test_isinstance_basestring_list(fixer):
    b = "isinstance(x, [basestring, dict])"
    a = "isinstance(x, [str, dict])"
    fixer.check(b, a)

    b = "isinstance(x, [dict, basestring])"
    a = "isinstance(x, [dict, str])"
    fixer.check(b, a)


def test_ensure_past_builtins_basestring_unchanged(fixer):
    u = "from past.builtins import basestring"
    fixer.unchanged(u)


def test_does_not_change_basestring_in_string(fixer):
    u = 'print("hello basestring")'
    fixer.unchanged(u)


def test_does_not_change_basestring_in_methodname(fixer):
    u = "return encode_basestring('foo')"
    fixer.unchanged(u)


def test_does_not_change_variable_assignments(fixer):
    u = "basestring = str"
    fixer.unchanged(u)
