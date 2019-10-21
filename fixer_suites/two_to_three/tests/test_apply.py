from .util import FixerTestCase


class Test_apply(FixerTestCase):
    fixer = "apply"

    def test_1(self):
        b = """x = apply(f, g + h)"""
        a = """x = f(*g + h)"""
        self.check(b, a)

    def test_2(self):
        b = """y = apply(f, g, h)"""
        a = """y = f(*g, **h)"""
        self.check(b, a)

    def test_3(self):
        b = """z = apply(fs[0], g or h, h or g)"""
        a = """z = fs[0](*g or h, **h or g)"""
        self.check(b, a)

    def test_4(self):
        b = """apply(f, (x, y) + t)"""
        a = """f(*(x, y) + t)"""
        self.check(b, a)

    def test_5(self):
        b = """apply(f, args,)"""
        a = """f(*args)"""
        self.check(b, a)

    def test_6(self):
        b = """apply(f, args, kwds,)"""
        a = """f(*args, **kwds)"""
        self.check(b, a)

    # Test that complex functions are parenthesized

    def test_complex_1(self):
        b = """x = apply(f+g, args)"""
        a = """x = (f+g)(*args)"""
        self.check(b, a)

    def test_complex_2(self):
        b = """x = apply(f*g, args)"""
        a = """x = (f*g)(*args)"""
        self.check(b, a)

    def test_complex_3(self):
        b = """x = apply(f**g, args)"""
        a = """x = (f**g)(*args)"""
        self.check(b, a)

    # But dotted names etc. not

    def test_dotted_name(self):
        b = """x = apply(f.g, args)"""
        a = """x = f.g(*args)"""
        self.check(b, a)

    def test_subscript(self):
        b = """x = apply(f[x], args)"""
        a = """x = f[x](*args)"""
        self.check(b, a)

    def test_call(self):
        b = """x = apply(f(), args)"""
        a = """x = f()(*args)"""
        self.check(b, a)

    # Extreme case
    def test_extreme(self):
        b = """x = apply(a.b.c.d.e.f, args, kwds)"""
        a = """x = a.b.c.d.e.f(*args, **kwds)"""
        self.check(b, a)

    # XXX Comments in weird places still get lost
    def test_weird_comments(self):
        b = """apply(   # foo
          f, # bar
          args)"""
        a = """f(*args)"""
        self.check(b, a)

    # These should *not* be touched

    def test_unchanged_1(self):
        s = """apply()"""
        self.unchanged(s)

    def test_unchanged_2(self):
        s = """apply(f)"""
        self.unchanged(s)

    def test_unchanged_3(self):
        s = """apply(f,)"""
        self.unchanged(s)

    def test_unchanged_4(self):
        s = """apply(f, args, kwds, extras)"""
        self.unchanged(s)

    def test_unchanged_5(self):
        s = """apply(f, *args, **kwds)"""
        self.unchanged(s)

    def test_unchanged_6(self):
        s = """apply(f, *args)"""
        self.unchanged(s)

    def test_unchanged_6b(self):
        s = """apply(f, **kwds)"""
        self.unchanged(s)

    def test_unchanged_7(self):
        s = """apply(func=f, args=args, kwds=kwds)"""
        self.unchanged(s)

    def test_unchanged_8(self):
        s = """apply(f, args=args, kwds=kwds)"""
        self.unchanged(s)

    def test_unchanged_9(self):
        s = """apply(f, args, kwds=kwds)"""
        self.unchanged(s)

    def test_space_1(self):
        a = """apply(  f,  args,   kwds)"""
        b = """f(*args, **kwds)"""
        self.check(a, b)

    def test_space_2(self):
        a = """apply(  f  ,args,kwds   )"""
        b = """f(*args, **kwds)"""
        self.check(a, b)
