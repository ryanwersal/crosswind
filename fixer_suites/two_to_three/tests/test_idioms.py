from .util import FixerTestCase


class Test_idioms(FixerTestCase):
    fixer = "idioms"

    def test_while(self):
        b = """while 1: foo()"""
        a = """while True: foo()"""
        self.check(b, a)

        b = """while   1: foo()"""
        a = """while   True: foo()"""
        self.check(b, a)

        b = """
            while 1:
                foo()
            """
        a = """
            while True:
                foo()
            """
        self.check(b, a)

    def test_while_unchanged(self):
        s = """while 11: foo()"""
        self.unchanged(s)

        s = """while 0: foo()"""
        self.unchanged(s)

        s = """while foo(): foo()"""
        self.unchanged(s)

        s = """while []: foo()"""
        self.unchanged(s)

    def test_eq_simple(self):
        b = """type(x) == T"""
        a = """isinstance(x, T)"""
        self.check(b, a)

        b = """if   type(x) == T: pass"""
        a = """if   isinstance(x, T): pass"""
        self.check(b, a)

    def test_eq_reverse(self):
        b = """T == type(x)"""
        a = """isinstance(x, T)"""
        self.check(b, a)

        b = """if   T == type(x): pass"""
        a = """if   isinstance(x, T): pass"""
        self.check(b, a)

    def test_eq_expression(self):
        b = """type(x+y) == d.get('T')"""
        a = """isinstance(x+y, d.get('T'))"""
        self.check(b, a)

        b = """type(   x  +  y) == d.get('T')"""
        a = """isinstance(x  +  y, d.get('T'))"""
        self.check(b, a)

    def test_is_simple(self):
        b = """type(x) is T"""
        a = """isinstance(x, T)"""
        self.check(b, a)

        b = """if   type(x) is T: pass"""
        a = """if   isinstance(x, T): pass"""
        self.check(b, a)

    def test_is_reverse(self):
        b = """T is type(x)"""
        a = """isinstance(x, T)"""
        self.check(b, a)

        b = """if   T is type(x): pass"""
        a = """if   isinstance(x, T): pass"""
        self.check(b, a)

    def test_is_expression(self):
        b = """type(x+y) is d.get('T')"""
        a = """isinstance(x+y, d.get('T'))"""
        self.check(b, a)

        b = """type(   x  +  y) is d.get('T')"""
        a = """isinstance(x  +  y, d.get('T'))"""
        self.check(b, a)

    def test_is_not_simple(self):
        b = """type(x) is not T"""
        a = """not isinstance(x, T)"""
        self.check(b, a)

        b = """if   type(x) is not T: pass"""
        a = """if   not isinstance(x, T): pass"""
        self.check(b, a)

    def test_is_not_reverse(self):
        b = """T is not type(x)"""
        a = """not isinstance(x, T)"""
        self.check(b, a)

        b = """if   T is not type(x): pass"""
        a = """if   not isinstance(x, T): pass"""
        self.check(b, a)

    def test_is_not_expression(self):
        b = """type(x+y) is not d.get('T')"""
        a = """not isinstance(x+y, d.get('T'))"""
        self.check(b, a)

        b = """type(   x  +  y) is not d.get('T')"""
        a = """not isinstance(x  +  y, d.get('T'))"""
        self.check(b, a)

    def test_ne_simple(self):
        b = """type(x) != T"""
        a = """not isinstance(x, T)"""
        self.check(b, a)

        b = """if   type(x) != T: pass"""
        a = """if   not isinstance(x, T): pass"""
        self.check(b, a)

    def test_ne_reverse(self):
        b = """T != type(x)"""
        a = """not isinstance(x, T)"""
        self.check(b, a)

        b = """if   T != type(x): pass"""
        a = """if   not isinstance(x, T): pass"""
        self.check(b, a)

    def test_ne_expression(self):
        b = """type(x+y) != d.get('T')"""
        a = """not isinstance(x+y, d.get('T'))"""
        self.check(b, a)

        b = """type(   x  +  y) != d.get('T')"""
        a = """not isinstance(x  +  y, d.get('T'))"""
        self.check(b, a)

    def test_type_unchanged(self):
        a = """type(x).__name__"""
        self.unchanged(a)

    def test_sort_list_call(self):
        b = """
            v = list(t)
            v.sort()
            foo(v)
            """
        a = """
            v = sorted(t)
            foo(v)
            """
        self.check(b, a)

        b = """
            v = list(foo(b) + d)
            v.sort()
            foo(v)
            """
        a = """
            v = sorted(foo(b) + d)
            foo(v)
            """
        self.check(b, a)

        b = """
            while x:
                v = list(t)
                v.sort()
                foo(v)
            """
        a = """
            while x:
                v = sorted(t)
                foo(v)
            """
        self.check(b, a)

        b = """
            v = list(t)
            # foo
            v.sort()
            foo(v)
            """
        a = """
            v = sorted(t)
            # foo
            foo(v)
            """
        self.check(b, a)

        b = r"""
            v = list(   t)
            v.sort()
            foo(v)
            """
        a = r"""
            v = sorted(   t)
            foo(v)
            """
        self.check(b, a)

        b = r"""
            try:
                m = list(s)
                m.sort()
            except: pass
            """

        a = r"""
            try:
                m = sorted(s)
            except: pass
            """
        self.check(b, a)

        b = r"""
            try:
                m = list(s)
                # foo
                m.sort()
            except: pass
            """

        a = r"""
            try:
                m = sorted(s)
                # foo
            except: pass
            """
        self.check(b, a)

        b = r"""
            m = list(s)
            # more comments
            m.sort()"""

        a = r"""
            m = sorted(s)
            # more comments"""
        self.check(b, a)

    def test_sort_simple_expr(self):
        b = """
            v = t
            v.sort()
            foo(v)
            """
        a = """
            v = sorted(t)
            foo(v)
            """
        self.check(b, a)

        b = """
            v = foo(b)
            v.sort()
            foo(v)
            """
        a = """
            v = sorted(foo(b))
            foo(v)
            """
        self.check(b, a)

        b = """
            v = b.keys()
            v.sort()
            foo(v)
            """
        a = """
            v = sorted(b.keys())
            foo(v)
            """
        self.check(b, a)

        b = """
            v = foo(b) + d
            v.sort()
            foo(v)
            """
        a = """
            v = sorted(foo(b) + d)
            foo(v)
            """
        self.check(b, a)

        b = """
            while x:
                v = t
                v.sort()
                foo(v)
            """
        a = """
            while x:
                v = sorted(t)
                foo(v)
            """
        self.check(b, a)

        b = """
            v = t
            # foo
            v.sort()
            foo(v)
            """
        a = """
            v = sorted(t)
            # foo
            foo(v)
            """
        self.check(b, a)

        b = r"""
            v =   t
            v.sort()
            foo(v)
            """
        a = r"""
            v =   sorted(t)
            foo(v)
            """
        self.check(b, a)

    def test_sort_unchanged(self):
        s = """
            v = list(t)
            w.sort()
            foo(w)
            """
        self.unchanged(s)

        s = """
            v = list(t)
            v.sort(u)
            foo(v)
            """
        self.unchanged(s)
