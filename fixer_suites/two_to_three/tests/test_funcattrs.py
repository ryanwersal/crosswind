import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(two_to_three_test_case):
    return two_to_three_test_case("funcattrs")


attrs = ["closure", "doc", "name", "defaults", "code", "globals", "dict"]


def test(fixer):
    for attr in attrs:
        b = "a.func_%s" % attr
        a = "a.__%s__" % attr
        fixer.check(b, a)

        b = "self.foo.func_%s.foo_bar" % attr
        a = "self.foo.__%s__.foo_bar" % attr
        fixer.check(b, a)


def test_unchanged(fixer):
    for attr in attrs:
        s = "foo(func_%s + 5)" % attr
        fixer.unchanged(s)

        s = "f(foo.__%s__)" % attr
        fixer.unchanged(s)

        s = "f(foo.__%s__.foo)" % attr
        fixer.unchanged(s)
