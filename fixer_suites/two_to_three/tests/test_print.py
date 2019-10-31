from crosswind import pygram
from crosswind.tests.support import FixerTestCase


class Test_print(FixerTestCase):
    fixer = "print"

    def test_prefix_preservation(self):
        b = """print 1,   1+1,   1+1+1"""
        a = """print(1,   1+1,   1+1+1)"""
        self.check(b, a)

    def test_idempotency(self):
        s = """print()"""
        self.unchanged(s)

        s = """print('')"""
        self.unchanged(s)

    def test_idempotency_print_as_function(self):
        self.refactor.driver.grammar = pygram.python_grammar_no_print_statement
        s = """print(1, 1+1, 1+1+1)"""
        self.unchanged(s)

        s = """print()"""
        self.unchanged(s)

        s = """print('')"""
        self.unchanged(s)

    def test_1(self):
        b = """print 1, 1+1, 1+1+1"""
        a = """print(1, 1+1, 1+1+1)"""
        self.check(b, a)

    def test_2(self):
        b = """print 1, 2"""
        a = """print(1, 2)"""
        self.check(b, a)

    def test_3(self):
        b = """print"""
        a = """print()"""
        self.check(b, a)

    def test_4(self):
        # from bug 3000
        b = """print whatever; print"""
        a = """print(whatever); print()"""
        self.check(b, a)

    def test_5(self):
        b = """print; print whatever;"""
        a = """print(); print(whatever);"""
        self.check(b, a)

    def test_tuple(self):
        b = """print (a, b, c)"""
        a = """print((a, b, c))"""
        self.check(b, a)

    # trailing commas

    def test_trailing_comma_1(self):
        b = """print 1, 2, 3,"""
        a = """print(1, 2, 3, end=' ')"""
        self.check(b, a)

    def test_trailing_comma_2(self):
        b = """print 1, 2,"""
        a = """print(1, 2, end=' ')"""
        self.check(b, a)

    def test_trailing_comma_3(self):
        b = """print 1,"""
        a = """print(1, end=' ')"""
        self.check(b, a)

    # >> stuff

    def test_vargs_without_trailing_comma(self):
        b = """print >>sys.stderr, 1, 2, 3"""
        a = """print(1, 2, 3, file=sys.stderr)"""
        self.check(b, a)

    def test_with_trailing_comma(self):
        b = """print >>sys.stderr, 1, 2,"""
        a = """print(1, 2, end=' ', file=sys.stderr)"""
        self.check(b, a)

    def test_no_trailing_comma(self):
        b = """print >>sys.stderr, 1+1"""
        a = """print(1+1, file=sys.stderr)"""
        self.check(b, a)

    def test_spaces_before_file(self):
        b = """print >>  sys.stderr"""
        a = """print(file=sys.stderr)"""
        self.check(b, a)

    def test_with_future_print_function(self):
        s = "from __future__ import print_function\n" "print('Hai!', end=' ')"
        self.unchanged(s)

        b = "print 'Hello, world!'"
        a = "print('Hello, world!')"
        self.check(b, a)
