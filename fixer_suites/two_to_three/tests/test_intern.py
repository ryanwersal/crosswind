from crosswind.tests.support import FixerTestCase


class Test_intern(FixerTestCase):
    fixer = "intern"

    def test_prefix_preservation(self):
        b = """x =   intern(  a  )"""
        a = """import sys\nx =   sys.intern(  a  )"""
        self.check(b, a)

        b = """y = intern("b" # test
              )"""
        a = """import sys\ny = sys.intern("b" # test
              )"""
        self.check(b, a)

        b = """z = intern(a+b+c.d,   )"""
        a = """import sys\nz = sys.intern(a+b+c.d,   )"""
        self.check(b, a)

    def test(self):
        b = """x = intern(a)"""
        a = """import sys\nx = sys.intern(a)"""
        self.check(b, a)

        b = """z = intern(a+b+c.d,)"""
        a = """import sys\nz = sys.intern(a+b+c.d,)"""
        self.check(b, a)

        b = """intern("y%s" % 5).replace("y", "")"""
        a = """import sys\nsys.intern("y%s" % 5).replace("y", "")"""
        self.check(b, a)

    # These should not be refactored

    def test_unchanged(self):
        s = """intern(a=1)"""
        self.unchanged(s)

        s = """intern(f, g)"""
        self.unchanged(s)

        s = """intern(*h)"""
        self.unchanged(s)

        s = """intern(**i)"""
        self.unchanged(s)

        s = """intern()"""
        self.unchanged(s)
