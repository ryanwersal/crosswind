from .util import FixerTestCase


class Test_standarderror(FixerTestCase):
    fixer = "standarderror"

    def test(self):
        b = """x =    StandardError()"""
        a = """x =    Exception()"""
        self.check(b, a)

        b = """x = StandardError(a, b, c)"""
        a = """x = Exception(a, b, c)"""
        self.check(b, a)

        b = """f(2 + StandardError(a, b, c))"""
        a = """f(2 + Exception(a, b, c))"""
        self.check(b, a)
