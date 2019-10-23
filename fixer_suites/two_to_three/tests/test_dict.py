from crosswind import fixer_util

from .util import FixerTestCase


class Test_dict(FixerTestCase):
    fixer = "dict"

    def test_prefix_preservation(self):
        b = "if   d. keys  (  )  : pass"
        a = "if   list(d. keys  (  ))  : pass"
        self.check(b, a)

        b = "if   d. items  (  )  : pass"
        a = "if   list(d. items  (  ))  : pass"
        self.check(b, a)

        b = "if   d. iterkeys  ( )  : pass"
        a = "if   iter(d. keys  ( ))  : pass"
        self.check(b, a)

        b = "[i for i in    d.  iterkeys(  )  ]"
        a = "[i for i in    d.  keys(  )  ]"
        self.check(b, a)

        b = "if   d. viewkeys  ( )  : pass"
        a = "if   d. keys  ( )  : pass"
        self.check(b, a)

        b = "[i for i in    d.  viewkeys(  )  ]"
        a = "[i for i in    d.  keys(  )  ]"
        self.check(b, a)

    def test_trailing_comment(self):
        b = "d.keys() # foo"
        a = "list(d.keys()) # foo"
        self.check(b, a)

        b = "d.items()  # foo"
        a = "list(d.items())  # foo"
        self.check(b, a)

        b = "d.iterkeys()  # foo"
        a = "iter(d.keys())  # foo"
        self.check(b, a)

        b = """[i for i in d.iterkeys() # foo
               ]"""
        a = """[i for i in d.keys() # foo
               ]"""
        self.check(b, a)

        b = """[i for i in d.iterkeys() # foo
               ]"""
        a = """[i for i in d.keys() # foo
               ]"""
        self.check(b, a)

        b = "d.viewitems()  # foo"
        a = "d.items()  # foo"
        self.check(b, a)

    def test_unchanged(self):
        for wrapper in fixer_util.consuming_calls:
            s = "s = %s(d.keys())" % wrapper
            self.unchanged(s)

            s = "s = %s(d.values())" % wrapper
            self.unchanged(s)

            s = "s = %s(d.items())" % wrapper
            self.unchanged(s)

    def test_01(self):
        b = "d.keys()"
        a = "list(d.keys())"
        self.check(b, a)

        b = "a[0].foo().keys()"
        a = "list(a[0].foo().keys())"
        self.check(b, a)

    def test_02(self):
        b = "d.items()"
        a = "list(d.items())"
        self.check(b, a)

    def test_03(self):
        b = "d.values()"
        a = "list(d.values())"
        self.check(b, a)

    def test_04(self):
        b = "d.iterkeys()"
        a = "iter(d.keys())"
        self.check(b, a)

    def test_05(self):
        b = "d.iteritems()"
        a = "iter(d.items())"
        self.check(b, a)

    def test_06(self):
        b = "d.itervalues()"
        a = "iter(d.values())"
        self.check(b, a)

    def test_07(self):
        s = "list(d.keys())"
        self.unchanged(s)

    def test_08(self):
        s = "sorted(d.keys())"
        self.unchanged(s)

    def test_09(self):
        b = "iter(d.keys())"
        a = "iter(list(d.keys()))"
        self.check(b, a)

    def test_10(self):
        b = "foo(d.keys())"
        a = "foo(list(d.keys()))"
        self.check(b, a)

    def test_11(self):
        b = "for i in d.keys(): print i"
        a = "for i in list(d.keys()): print i"
        self.check(b, a)

    def test_12(self):
        b = "for i in d.iterkeys(): print i"
        a = "for i in d.keys(): print i"
        self.check(b, a)

    def test_13(self):
        b = "[i for i in d.keys()]"
        a = "[i for i in list(d.keys())]"
        self.check(b, a)

    def test_14(self):
        b = "[i for i in d.iterkeys()]"
        a = "[i for i in d.keys()]"
        self.check(b, a)

    def test_15(self):
        b = "(i for i in d.keys())"
        a = "(i for i in list(d.keys()))"
        self.check(b, a)

    def test_16(self):
        b = "(i for i in d.iterkeys())"
        a = "(i for i in d.keys())"
        self.check(b, a)

    def test_17(self):
        b = "iter(d.iterkeys())"
        a = "iter(d.keys())"
        self.check(b, a)

    def test_18(self):
        b = "list(d.iterkeys())"
        a = "list(d.keys())"
        self.check(b, a)

    def test_19(self):
        b = "sorted(d.iterkeys())"
        a = "sorted(d.keys())"
        self.check(b, a)

    def test_20(self):
        b = "foo(d.iterkeys())"
        a = "foo(iter(d.keys()))"
        self.check(b, a)

    def test_21(self):
        b = "print h.iterkeys().next()"
        a = "print iter(h.keys()).next()"
        self.check(b, a)

    def test_22(self):
        b = "print h.keys()[0]"
        a = "print list(h.keys())[0]"
        self.check(b, a)

    def test_23(self):
        b = "print list(h.iterkeys().next())"
        a = "print list(iter(h.keys()).next())"
        self.check(b, a)

    def test_24(self):
        b = "for x in h.keys()[0]: print x"
        a = "for x in list(h.keys())[0]: print x"
        self.check(b, a)

    def test_25(self):
        b = "d.viewkeys()"
        a = "d.keys()"
        self.check(b, a)

    def test_26(self):
        b = "d.viewitems()"
        a = "d.items()"
        self.check(b, a)

    def test_27(self):
        b = "d.viewvalues()"
        a = "d.values()"
        self.check(b, a)

    def test_28(self):
        b = "[i for i in d.viewkeys()]"
        a = "[i for i in d.keys()]"
        self.check(b, a)

    def test_29(self):
        b = "(i for i in d.viewkeys())"
        a = "(i for i in d.keys())"
        self.check(b, a)

    def test_30(self):
        b = "iter(d.viewkeys())"
        a = "iter(d.keys())"
        self.check(b, a)

    def test_31(self):
        b = "list(d.viewkeys())"
        a = "list(d.keys())"
        self.check(b, a)

    def test_32(self):
        b = "sorted(d.viewkeys())"
        a = "sorted(d.keys())"
        self.check(b, a)
