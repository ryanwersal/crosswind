from .util import FixerTestCase


class Test_basestring(FixerTestCase):
    fixer = "basestring"

    def test_basestring(self):
        b = """isinstance(x, basestring)"""
        a = """isinstance(x, str)"""
        self.check(b, a)
