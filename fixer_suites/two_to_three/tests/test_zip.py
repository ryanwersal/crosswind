from .util import FixerTestCase


class Test_zip(FixerTestCase):
    fixer = "zip"

    def check(self, b, a):
        self.unchanged("from future_builtins import zip; " + b, a)
        super(Test_zip, self).check(b, a)

    def test_zip_basic(self):
        b = """x = zip()"""
        a = """x = list(zip())"""
        self.check(b, a)

        b = """x = zip(a, b, c)"""
        a = """x = list(zip(a, b, c))"""
        self.check(b, a)

        b = """x = len(zip(a, b))"""
        a = """x = len(list(zip(a, b)))"""
        self.check(b, a)

    def test_zip_trailers(self):
        b = """x = zip(a, b, c)[0]"""
        a = """x = list(zip(a, b, c))[0]"""
        self.check(b, a)

        b = """x = zip(a, b, c)[0][1]"""
        a = """x = list(zip(a, b, c))[0][1]"""
        self.check(b, a)

    def test_zip_nochange(self):
        a = """b.join(zip(a, b))"""
        self.unchanged(a)
        a = """(a + foo(5)).join(zip(a, b))"""
        self.unchanged(a)
        a = """iter(zip(a, b))"""
        self.unchanged(a)
        a = """list(zip(a, b))"""
        self.unchanged(a)
        a = """list(zip(a, b))[0]"""
        self.unchanged(a)
        a = """set(zip(a, b))"""
        self.unchanged(a)
        a = """set(zip(a, b)).pop()"""
        self.unchanged(a)
        a = """tuple(zip(a, b))"""
        self.unchanged(a)
        a = """any(zip(a, b))"""
        self.unchanged(a)
        a = """all(zip(a, b))"""
        self.unchanged(a)
        a = """sum(zip(a, b))"""
        self.unchanged(a)
        a = """sorted(zip(a, b))"""
        self.unchanged(a)
        a = """sorted(zip(a, b), key=blah)"""
        self.unchanged(a)
        a = """sorted(zip(a, b), key=blah)[0]"""
        self.unchanged(a)
        a = """enumerate(zip(a, b))"""
        self.unchanged(a)
        a = """enumerate(zip(a, b), start=1)"""
        self.unchanged(a)
        a = """for i in zip(a, b): pass"""
        self.unchanged(a)
        a = """[x for x in zip(a, b)]"""
        self.unchanged(a)
        a = """(x for x in zip(a, b))"""
        self.unchanged(a)

    def test_future_builtins(self):
        a = "from future_builtins import spam, zip, eggs; zip(a, b)"
        self.unchanged(a)

        b = """from future_builtins import spam, eggs; x = zip(a, b)"""
        a = """from future_builtins import spam, eggs; x = list(zip(a, b))"""
        self.check(b, a)

        a = "from future_builtins import *; zip(a, b)"
        self.unchanged(a)
