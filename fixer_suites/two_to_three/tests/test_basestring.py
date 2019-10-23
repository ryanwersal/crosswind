from .util import FixerTestCase


class Test_basestring(FixerTestCase):
    fixer = "basestring"

    def test_basestring(self):
        b = """isinstance(x, basestring)"""
        a = """isinstance(x, str)"""
        self.check(b, a)

    def test_ensure_past_builtins_basestring_unchanged(self):
        u = "from past.builtins import basestring"
        self.unchanged(u)

    def test_does_not_change_basestring_in_string(self):
        u = 'print("hello basestring")'
        self.unchanged(u)

    def test_does_not_change_basestring_in_methodname(self):
        u = "return encode_basestring('foo')"
        self.unchanged(u)
