from crosswind.tests.support import FixerTestCase


class Test_long(FixerTestCase):
    fixer = "long"

    def test_1(self):
        b = """x = long(x)"""
        a = """x = int(x)"""
        self.check(b, a)

    def test_2(self):
        b = """y = isinstance(x, long)"""
        a = """y = isinstance(x, int)"""
        self.check(b, a)

    def test_3(self):
        b = """z = type(x) in (int, long)"""
        a = """z = type(x) in (int, int)"""
        self.check(b, a)

    def test_unchanged(self):
        s = """long = True"""
        self.unchanged(s)

        s = """s.long = True"""
        self.unchanged(s)

        s = """def long(): pass"""
        self.unchanged(s)

        s = """class long(): pass"""
        self.unchanged(s)

        s = """def f(long): pass"""
        self.unchanged(s)

        s = """def f(g, long): pass"""
        self.unchanged(s)

        s = """def f(x, long=True): pass"""
        self.unchanged(s)

    def test_prefix_preservation(self):
        b = """x =   long(  x  )"""
        a = """x =   int(  x  )"""
        self.check(b, a)
