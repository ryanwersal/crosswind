from .util import FixerTestCase


class Test_methodattrs(FixerTestCase):
    fixer = "methodattrs"

    attrs = ["func", "self", "class"]

    def test(self):
        for attr in self.attrs:
            b = "a.im_%s" % attr
            if attr == "class":
                a = "a.__self__.__class__"
            else:
                a = "a.__%s__" % attr
            self.check(b, a)

            b = "self.foo.im_%s.foo_bar" % attr
            if attr == "class":
                a = "self.foo.__self__.__class__.foo_bar"
            else:
                a = "self.foo.__%s__.foo_bar" % attr
            self.check(b, a)

    def test_unchanged(self):
        for attr in self.attrs:
            s = "foo(im_%s + 5)" % attr
            self.unchanged(s)

            s = "f(foo.__%s__)" % attr
            self.unchanged(s)

            s = "f(foo.__%s__.foo)" % attr
            self.unchanged(s)
