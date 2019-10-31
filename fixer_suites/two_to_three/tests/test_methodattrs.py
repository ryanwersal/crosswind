import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(two_to_three_test_case):
    return two_to_three_test_case("methodattrs")


attrs = ["func", "self", "class"]


def test(fixer):
    for attr in attrs:
        b = "a.im_%s" % attr
        if attr == "class":
            a = "a.__self__.__class__"
        else:
            a = "a.__%s__" % attr
        fixer.check(b, a)

        b = "self.foo.im_%s.foo_bar" % attr
        if attr == "class":
            a = "self.foo.__self__.__class__.foo_bar"
        else:
            a = "self.foo.__%s__.foo_bar" % attr
        fixer.check(b, a)


def test_unchanged(fixer):
    for attr in attrs:
        s = "foo(im_%s + 5)" % attr
        fixer.unchanged(s)

        s = "f(foo.__%s__)" % attr
        fixer.unchanged(s)

        s = "f(foo.__%s__.foo)" % attr
        fixer.unchanged(s)
