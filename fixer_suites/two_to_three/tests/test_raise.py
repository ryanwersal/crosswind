from .util import FixerTestCase


class Test_raise(FixerTestCase):
    fixer = "raise"

    def test_basic(self):
        b = """raise Exception, 5"""
        a = """raise Exception(5)"""
        self.check(b, a)

    def test_prefix_preservation(self):
        b = """raise Exception,5"""
        a = """raise Exception(5)"""
        self.check(b, a)

        b = """raise   Exception,    5"""
        a = """raise   Exception(5)"""
        self.check(b, a)

    def test_with_comments(self):
        b = """raise Exception, 5 # foo"""
        a = """raise Exception(5) # foo"""
        self.check(b, a)

        b = """raise E, (5, 6) % (a, b) # foo"""
        a = """raise E((5, 6) % (a, b)) # foo"""
        self.check(b, a)

        b = """def foo():
                    raise Exception, 5, 6 # foo"""
        a = """def foo():
                    raise Exception(5).with_traceback(6) # foo"""
        self.check(b, a)

    def test_None_value(self):
        b = """raise Exception(5), None, tb"""
        a = """raise Exception(5).with_traceback(tb)"""
        self.check(b, a)

    def test_tuple_value(self):
        b = """raise Exception, (5, 6, 7)"""
        a = """raise Exception(5, 6, 7)"""
        self.check(b, a)

    def test_tuple_detection(self):
        b = """raise E, (5, 6) % (a, b)"""
        a = """raise E((5, 6) % (a, b))"""
        self.check(b, a)

    def test_tuple_exc_1(self):
        b = """raise (((E1, E2), E3), E4), V"""
        a = """raise E1(V)"""
        self.check(b, a)

    def test_tuple_exc_2(self):
        b = """raise (E1, (E2, E3), E4), V"""
        a = """raise E1(V)"""
        self.check(b, a)

    # These should produce a warning

    def test_string_exc(self):
        s = """raise 'foo'"""
        self.warns_unchanged(s, "Python 3 does not support string exceptions")

    def test_string_exc_val(self):
        s = """raise "foo", 5"""
        self.warns_unchanged(s, "Python 3 does not support string exceptions")

    def test_string_exc_val_tb(self):
        s = """raise "foo", 5, 6"""
        self.warns_unchanged(s, "Python 3 does not support string exceptions")

    # These should result in traceback-assignment

    def test_tb_1(self):
        b = """def foo():
                    raise Exception, 5, 6"""
        a = """def foo():
                    raise Exception(5).with_traceback(6)"""
        self.check(b, a)

    def test_tb_2(self):
        b = """def foo():
                    a = 5
                    raise Exception, 5, 6
                    b = 6"""
        a = """def foo():
                    a = 5
                    raise Exception(5).with_traceback(6)
                    b = 6"""
        self.check(b, a)

    def test_tb_3(self):
        b = """def foo():
                    raise Exception,5,6"""
        a = """def foo():
                    raise Exception(5).with_traceback(6)"""
        self.check(b, a)

    def test_tb_4(self):
        b = """def foo():
                    a = 5
                    raise Exception,5,6
                    b = 6"""
        a = """def foo():
                    a = 5
                    raise Exception(5).with_traceback(6)
                    b = 6"""
        self.check(b, a)

    def test_tb_5(self):
        b = """def foo():
                    raise Exception, (5, 6, 7), 6"""
        a = """def foo():
                    raise Exception(5, 6, 7).with_traceback(6)"""
        self.check(b, a)

    def test_tb_6(self):
        b = """def foo():
                    a = 5
                    raise Exception, (5, 6, 7), 6
                    b = 6"""
        a = """def foo():
                    a = 5
                    raise Exception(5, 6, 7).with_traceback(6)
                    b = 6"""
        self.check(b, a)
