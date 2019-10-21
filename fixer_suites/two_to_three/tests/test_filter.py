from .util import FixerTestCase


class Test_filter(FixerTestCase):
    fixer = "filter"

    def test_prefix_preservation(self):
        b = """x =   filter(    foo,     'abc'   )"""
        a = """x =   list(filter(    foo,     'abc'   ))"""
        self.check(b, a)

        b = """x =   filter(  None , 'abc'  )"""
        a = """x =   [_f for _f in 'abc' if _f]"""
        self.check(b, a)

    def test_filter_basic(self):
        b = """x = filter(None, 'abc')"""
        a = """x = [_f for _f in 'abc' if _f]"""
        self.check(b, a)

        b = """x = len(filter(f, 'abc'))"""
        a = """x = len(list(filter(f, 'abc')))"""
        self.check(b, a)

        b = """x = filter(lambda x: x%2 == 0, range(10))"""
        a = """x = [x for x in range(10) if x%2 == 0]"""
        self.check(b, a)

        # Note the parens around x
        b = """x = filter(lambda (x): x%2 == 0, range(10))"""
        a = """x = [x for x in range(10) if x%2 == 0]"""
        self.check(b, a)

    def test_filter_trailers(self):
        b = """x = filter(None, 'abc')[0]"""
        a = """x = [_f for _f in 'abc' if _f][0]"""
        self.check(b, a)

        b = """x = len(filter(f, 'abc')[0])"""
        a = """x = len(list(filter(f, 'abc'))[0])"""
        self.check(b, a)

        b = """x = filter(lambda x: x%2 == 0, range(10))[0]"""
        a = """x = [x for x in range(10) if x%2 == 0][0]"""
        self.check(b, a)

        # Note the parens around x
        b = """x = filter(lambda (x): x%2 == 0, range(10))[0]"""
        a = """x = [x for x in range(10) if x%2 == 0][0]"""
        self.check(b, a)

    def test_filter_nochange(self):
        a = """b.join(filter(f, 'abc'))"""
        self.unchanged(a)
        a = """(a + foo(5)).join(filter(f, 'abc'))"""
        self.unchanged(a)
        a = """iter(filter(f, 'abc'))"""
        self.unchanged(a)
        a = """list(filter(f, 'abc'))"""
        self.unchanged(a)
        a = """list(filter(f, 'abc'))[0]"""
        self.unchanged(a)
        a = """set(filter(f, 'abc'))"""
        self.unchanged(a)
        a = """set(filter(f, 'abc')).pop()"""
        self.unchanged(a)
        a = """tuple(filter(f, 'abc'))"""
        self.unchanged(a)
        a = """any(filter(f, 'abc'))"""
        self.unchanged(a)
        a = """all(filter(f, 'abc'))"""
        self.unchanged(a)
        a = """sum(filter(f, 'abc'))"""
        self.unchanged(a)
        a = """sorted(filter(f, 'abc'))"""
        self.unchanged(a)
        a = """sorted(filter(f, 'abc'), key=blah)"""
        self.unchanged(a)
        a = """sorted(filter(f, 'abc'), key=blah)[0]"""
        self.unchanged(a)
        a = """enumerate(filter(f, 'abc'))"""
        self.unchanged(a)
        a = """enumerate(filter(f, 'abc'), start=1)"""
        self.unchanged(a)
        a = """for i in filter(f, 'abc'): pass"""
        self.unchanged(a)
        a = """[x for x in filter(f, 'abc')]"""
        self.unchanged(a)
        a = """(x for x in filter(f, 'abc'))"""
        self.unchanged(a)

    def test_future_builtins(self):
        a = "from future_builtins import spam, filter; filter(f, 'ham')"
        self.unchanged(a)

        b = """from future_builtins import spam; x = filter(f, 'abc')"""
        a = """from future_builtins import spam; x = list(filter(f, 'abc'))"""
        self.check(b, a)

        a = "from future_builtins import *; filter(f, 'ham')"
        self.unchanged(a)
