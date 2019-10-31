from crosswind.tests.support import FixerTestCase


class Test_reload(FixerTestCase):
    fixer = "reload"

    def test(self):
        b = """reload(a)"""
        a = """import importlib\nimportlib.reload(a)"""
        self.check(b, a)

    def test_comment(self):
        b = """reload( a ) # comment"""
        a = """import importlib\nimportlib.reload( a ) # comment"""
        self.check(b, a)

        # PEP 8 comments
        b = """reload( a )  # comment"""
        a = """import importlib\nimportlib.reload( a )  # comment"""
        self.check(b, a)

    def test_space(self):
        b = """reload( a )"""
        a = """import importlib\nimportlib.reload( a )"""
        self.check(b, a)

        b = """reload( a)"""
        a = """import importlib\nimportlib.reload( a)"""
        self.check(b, a)

        b = """reload(a )"""
        a = """import importlib\nimportlib.reload(a )"""
        self.check(b, a)

    def test_unchanged(self):
        s = """reload(a=1)"""
        self.unchanged(s)

        s = """reload(f, g)"""
        self.unchanged(s)

        s = """reload(f, *h)"""
        self.unchanged(s)

        s = """reload(f, *h, **i)"""
        self.unchanged(s)

        s = """reload(f, **i)"""
        self.unchanged(s)

        s = """reload(*h, **i)"""
        self.unchanged(s)

        s = """reload(*h)"""
        self.unchanged(s)

        s = """reload(**i)"""
        self.unchanged(s)

        s = """reload()"""
        self.unchanged(s)
