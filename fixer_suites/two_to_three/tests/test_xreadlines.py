from .util import FixerTestCase


class Test_xreadlines(FixerTestCase):
    fixer = "xreadlines"

    def test_call(self):
        b = "for x in f.xreadlines(): pass"
        a = "for x in f: pass"
        self.check(b, a)

        b = "for x in foo().xreadlines(): pass"
        a = "for x in foo(): pass"
        self.check(b, a)

        b = "for x in (5 + foo()).xreadlines(): pass"
        a = "for x in (5 + foo()): pass"
        self.check(b, a)

    def test_attr_ref(self):
        b = "foo(f.xreadlines + 5)"
        a = "foo(f.__iter__ + 5)"
        self.check(b, a)

        b = "foo(f().xreadlines + 5)"
        a = "foo(f().__iter__ + 5)"
        self.check(b, a)

        b = "foo((5 + f()).xreadlines + 5)"
        a = "foo((5 + f()).__iter__ + 5)"
        self.check(b, a)

    def test_unchanged(self):
        s = "for x in f.xreadlines(5): pass"
        self.unchanged(s)

        s = "for x in f.xreadlines(k=5): pass"
        self.unchanged(s)

        s = "for x in f.xreadlines(*k, **v): pass"
        self.unchanged(s)

        s = "foo(xreadlines)"
        self.unchanged(s)
