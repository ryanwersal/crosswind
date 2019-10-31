from crosswind import fixer_util
from crosswind.tests.support import FixerTestCase


class Test_xrange(FixerTestCase):
    fixer = "xrange"

    def test_prefix_preservation(self):
        b = """x =    xrange(  10  )"""
        a = """x =    range(  10  )"""
        self.check(b, a)

        b = """x = xrange(  1  ,  10   )"""
        a = """x = range(  1  ,  10   )"""
        self.check(b, a)

        b = """x = xrange(  0  ,  10 ,  2 )"""
        a = """x = range(  0  ,  10 ,  2 )"""
        self.check(b, a)

    def test_single_arg(self):
        b = """x = xrange(10)"""
        a = """x = range(10)"""
        self.check(b, a)

    def test_two_args(self):
        b = """x = xrange(1, 10)"""
        a = """x = range(1, 10)"""
        self.check(b, a)

    def test_three_args(self):
        b = """x = xrange(0, 10, 2)"""
        a = """x = range(0, 10, 2)"""
        self.check(b, a)

    def test_wrap_in_list(self):
        b = """x = range(10, 3, 9)"""
        a = """x = list(range(10, 3, 9))"""
        self.check(b, a)

        b = """x = foo(range(10, 3, 9))"""
        a = """x = foo(list(range(10, 3, 9)))"""
        self.check(b, a)

        b = """x = range(10, 3, 9) + [4]"""
        a = """x = list(range(10, 3, 9)) + [4]"""
        self.check(b, a)

        b = """x = range(10)[::-1]"""
        a = """x = list(range(10))[::-1]"""
        self.check(b, a)

        b = """x = range(10)  [3]"""
        a = """x = list(range(10))  [3]"""
        self.check(b, a)

    def test_xrange_in_for(self):
        b = """for i in xrange(10):\n    j=i"""
        a = """for i in range(10):\n    j=i"""
        self.check(b, a)

        b = """[i for i in xrange(10)]"""
        a = """[i for i in range(10)]"""
        self.check(b, a)

    def test_range_in_for(self):
        self.unchanged("for i in range(10): pass")
        self.unchanged("[i for i in range(10)]")

    def test_in_contains_test(self):
        self.unchanged("x in range(10, 3, 9)")

    def test_in_consuming_context(self):
        for call in fixer_util.consuming_calls:
            self.unchanged("a = %s(range(10))" % call)
