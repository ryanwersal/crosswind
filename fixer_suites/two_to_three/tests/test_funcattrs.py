from crosswind.tests.support import FixerTestCase


class Test_funcattrs(FixerTestCase):
    fixer = "funcattrs"

    attrs = ["closure", "doc", "name", "defaults", "code", "globals", "dict"]

    def test(self):
        for attr in self.attrs:
            b = "a.func_%s" % attr
            a = "a.__%s__" % attr
            self.check(b, a)

            b = "self.foo.func_%s.foo_bar" % attr
            a = "self.foo.__%s__.foo_bar" % attr
            self.check(b, a)

    def test_unchanged(self):
        for attr in self.attrs:
            s = "foo(func_%s + 5)" % attr
            self.unchanged(s)

            s = "f(foo.__%s__)" % attr
            self.unchanged(s)

            s = "f(foo.__%s__.foo)" % attr
            self.unchanged(s)
