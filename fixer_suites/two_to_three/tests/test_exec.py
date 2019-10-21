from .util import FixerTestCase


class Test_exec(FixerTestCase):
    fixer = "exec"

    def test_prefix_preservation(self):
        b = """  exec code in ns1,   ns2"""
        a = """  exec(code, ns1,   ns2)"""
        self.check(b, a)

    def test_basic(self):
        b = """exec code"""
        a = """exec(code)"""
        self.check(b, a)

    def test_with_globals(self):
        b = """exec code in ns"""
        a = """exec(code, ns)"""
        self.check(b, a)

    def test_with_globals_locals(self):
        b = """exec code in ns1, ns2"""
        a = """exec(code, ns1, ns2)"""
        self.check(b, a)

    def test_complex_1(self):
        b = """exec (a.b()) in ns"""
        a = """exec((a.b()), ns)"""
        self.check(b, a)

    def test_complex_2(self):
        b = """exec a.b() + c in ns"""
        a = """exec(a.b() + c, ns)"""
        self.check(b, a)

    # These should not be touched

    def test_unchanged_1(self):
        s = """exec(code)"""
        self.unchanged(s)

    def test_unchanged_2(self):
        s = """exec (code)"""
        self.unchanged(s)

    def test_unchanged_3(self):
        s = """exec(code, ns)"""
        self.unchanged(s)

    def test_unchanged_4(self):
        s = """exec(code, ns1, ns2)"""
        self.unchanged(s)
