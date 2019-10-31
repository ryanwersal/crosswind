import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(two_to_three_test_case):
    return two_to_three_test_case("xreadlines")


def test_call(fixer):
    b = "for x in f.xreadlines(): pass"
    a = "for x in f: pass"
    fixer.check(b, a)

    b = "for x in foo().xreadlines(): pass"
    a = "for x in foo(): pass"
    fixer.check(b, a)

    b = "for x in (5 + foo()).xreadlines(): pass"
    a = "for x in (5 + foo()): pass"
    fixer.check(b, a)


def test_attr_ref(fixer):
    b = "foo(f.xreadlines + 5)"
    a = "foo(f.__iter__ + 5)"
    fixer.check(b, a)

    b = "foo(f().xreadlines + 5)"
    a = "foo(f().__iter__ + 5)"
    fixer.check(b, a)

    b = "foo((5 + f()).xreadlines + 5)"
    a = "foo((5 + f()).__iter__ + 5)"
    fixer.check(b, a)


def test_unchanged(fixer):
    s = "for x in f.xreadlines(5): pass"
    fixer.unchanged(s)

    s = "for x in f.xreadlines(k=5): pass"
    fixer.unchanged(s)

    s = "for x in f.xreadlines(*k, **v): pass"
    fixer.unchanged(s)

    s = "foo(xreadlines)"
    fixer.unchanged(s)
