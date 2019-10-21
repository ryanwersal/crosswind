from .util import FixerTestCase


class Test_throw(FixerTestCase):
    fixer = "throw"

    def test_1(self):
        b = """g.throw(Exception, 5)"""
        a = """g.throw(Exception(5))"""
        self.check(b, a)

    def test_2(self):
        b = """g.throw(Exception,5)"""
        a = """g.throw(Exception(5))"""
        self.check(b, a)

    def test_3(self):
        b = """g.throw(Exception, (5, 6, 7))"""
        a = """g.throw(Exception(5, 6, 7))"""
        self.check(b, a)

    def test_4(self):
        b = """5 + g.throw(Exception, 5)"""
        a = """5 + g.throw(Exception(5))"""
        self.check(b, a)

    # These should produce warnings

    def test_warn_1(self):
        s = """g.throw("foo")"""
        self.warns_unchanged(s, "Python 3 does not support string exceptions")

    def test_warn_2(self):
        s = """g.throw("foo", 5)"""
        self.warns_unchanged(s, "Python 3 does not support string exceptions")

    def test_warn_3(self):
        s = """g.throw("foo", 5, 6)"""
        self.warns_unchanged(s, "Python 3 does not support string exceptions")

    # These should not be touched

    def test_untouched_1(self):
        s = """g.throw(Exception)"""
        self.unchanged(s)

    def test_untouched_2(self):
        s = """g.throw(Exception(5, 6))"""
        self.unchanged(s)

    def test_untouched_3(self):
        s = """5 + g.throw(Exception(5, 6))"""
        self.unchanged(s)

    # These should result in traceback-assignment

    def test_tb_1(self):
        b = """def foo():
                    g.throw(Exception, 5, 6)"""
        a = """def foo():
                    g.throw(Exception(5).with_traceback(6))"""
        self.check(b, a)

    def test_tb_2(self):
        b = """def foo():
                    a = 5
                    g.throw(Exception, 5, 6)
                    b = 6"""
        a = """def foo():
                    a = 5
                    g.throw(Exception(5).with_traceback(6))
                    b = 6"""
        self.check(b, a)

    def test_tb_3(self):
        b = """def foo():
                    g.throw(Exception,5,6)"""
        a = """def foo():
                    g.throw(Exception(5).with_traceback(6))"""
        self.check(b, a)

    def test_tb_4(self):
        b = """def foo():
                    a = 5
                    g.throw(Exception,5,6)
                    b = 6"""
        a = """def foo():
                    a = 5
                    g.throw(Exception(5).with_traceback(6))
                    b = 6"""
        self.check(b, a)

    def test_tb_5(self):
        b = """def foo():
                    g.throw(Exception, (5, 6, 7), 6)"""
        a = """def foo():
                    g.throw(Exception(5, 6, 7).with_traceback(6))"""
        self.check(b, a)

    def test_tb_6(self):
        b = """def foo():
                    a = 5
                    g.throw(Exception, (5, 6, 7), 6)
                    b = 6"""
        a = """def foo():
                    a = 5
                    g.throw(Exception(5, 6, 7).with_traceback(6))
                    b = 6"""
        self.check(b, a)

    def test_tb_7(self):
        b = """def foo():
                    a + g.throw(Exception, 5, 6)"""
        a = """def foo():
                    a + g.throw(Exception(5).with_traceback(6))"""
        self.check(b, a)

    def test_tb_8(self):
        b = """def foo():
                    a = 5
                    a + g.throw(Exception, 5, 6)
                    b = 6"""
        a = """def foo():
                    a = 5
                    a + g.throw(Exception(5).with_traceback(6))
                    b = 6"""
        self.check(b, a)
