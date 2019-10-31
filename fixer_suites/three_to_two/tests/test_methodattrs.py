import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(three_to_two_test_case):
    return three_to_two_test_case("methodattrs")


attrs = ["func", "self"]


def test_methodattrs(fixer):
    for attr in attrs:
        b = "a.__%s__" % attr
        a = "a.im_%s" % attr
        fixer.check(b, a)

        b = "self.foo.__%s__.foo_bar" % attr
        a = "self.foo.im_%s.foo_bar" % attr
        fixer.check(b, a)

        b = "dir(self.foo.__self__.__class__)"
        a = "dir(self.foo.im_self.__class__)"
        fixer.check(b, a)


def test_unchanged(fixer):
    for attr in attrs:
        s = "foo(__%s__ + 5)" % attr
        fixer.unchanged(s)
