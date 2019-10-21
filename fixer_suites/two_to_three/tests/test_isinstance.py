from .util import FixerTestCase


class Test_isinstance(FixerTestCase):
    fixer = "isinstance"

    def test_remove_multiple_items(self):
        b = """isinstance(x, (int, int, int))"""
        a = """isinstance(x, int)"""
        self.check(b, a)

        b = """isinstance(x, (int, float, int, int, float))"""
        a = """isinstance(x, (int, float))"""
        self.check(b, a)

        b = """isinstance(x, (int, float, int, int, float, str))"""
        a = """isinstance(x, (int, float, str))"""
        self.check(b, a)

        b = """isinstance(foo() + bar(), (x(), y(), x(), int, int))"""
        a = """isinstance(foo() + bar(), (x(), y(), x(), int))"""
        self.check(b, a)

    def test_prefix_preservation(self):
        b = """if    isinstance(  foo(), (  bar, bar, baz )) : pass"""
        a = """if    isinstance(  foo(), (  bar, baz )) : pass"""
        self.check(b, a)

    def test_unchanged(self):
        self.unchanged("isinstance(x, (str, int))")
