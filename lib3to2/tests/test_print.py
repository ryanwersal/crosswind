from lib3to2.tests.test_all_fixers import lib3to2FixerTestCase

class Test_print(lib3to2FixerTestCase):
    fixer = "print"

    def test_prefix_preservation(self):
        b = """print (1,   1+1,   1+1+1)"""
        a = """print 1,   1+1,   1+1+1"""
        self.check(b, a)

    def test_idempotency(self):
        s = """print()"""
        self.unchanged(s)

        s = """print('')"""
        self.unchanged(s)

    def test_1(self):
        b = """print (1, 1+1, 1+1+1)"""
        a = """print 1, 1+1, 1+1+1"""
        self.check(b, a)

    def test_2(self):
        b = """print(1, 2)"""
        a = """print 1, 2"""
        self.check(b, a)

    def test_3(self):
        # from bug 3000
        b = """print(whatever); print()"""
        a = """print whatever; print()"""
        self.check(b, a)

    def test_4(self):
        b = """print(); print (whatever);"""
        a = """print(); print whatever;"""

    def test_tuple(self):
        b = """print((a, b, c))"""
        a = """print (a, b, c)"""
        self.check(b, a)

    # trailing commas

    def test_trailing_comma_1(self):
        b = """print(1, 2, 3, end=' ')"""
        a = """print 1, 2, 3,"""
        self.check(b, a)

    def test_trailing_comma_2(self):
        b = """print(1, 2, end=' ')"""
        a = """print 1, 2,"""
        self.check(b, a)

    def test_trailing_comma_3(self):
        b = """print(1, end=' ')"""
        a = """print 1,"""
        self.check(b, a)

    # >> stuff

    def test_vargs_without_trailing_comma(self):
        b = """print(1, 2, 3, file=sys.stderr)"""
        a = """print >>sys.stderr, 1, 2, 3"""
        self.check(b, a)

    def test_with_trailing_comma(self):
        b = """print(1, 2, end=' ', file=sys.stderr)"""
        a = """print >>sys.stderr, 1, 2,"""
        self.check(b, a)

    def test_no_trailing_comma(self):
        b = """print(1+1, file=sys.stderr)"""
        a = """print >>sys.stderr, 1+1"""
        self.check(b, a)

    def test_spaces_before_file(self):
        b = """print(file=sys.stderr)"""
        a = """print >>  sys.stderr"""
        self.check(b, a)
