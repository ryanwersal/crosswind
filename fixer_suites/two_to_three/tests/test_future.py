from .util import FixerTestCase


class Test_future(FixerTestCase):
    fixer = "future"

    def test_future(self):
        b = """from __future__ import braces"""
        a = """"""
        self.check(b, a)

        b = """# comment\nfrom __future__ import braces"""
        a = """# comment\n"""
        self.check(b, a)

        b = """from __future__ import braces\n# comment"""
        a = """\n# comment"""
        self.check(b, a)

    def test_run_order(self):
        self.assert_runs_after("print")
