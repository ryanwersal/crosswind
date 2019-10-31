from crosswind.tests.support import FixerTestCase


class Test_paren(FixerTestCase):
    fixer = "paren"

    def test_0(self):
        b = """[i for i in 1, 2 ]"""
        a = """[i for i in (1, 2) ]"""
        self.check(b, a)

    def test_1(self):
        b = """[i for i in 1, 2, ]"""
        a = """[i for i in (1, 2,) ]"""
        self.check(b, a)

    def test_2(self):
        b = """[i for i  in     1, 2 ]"""
        a = """[i for i  in     (1, 2) ]"""
        self.check(b, a)

    def test_3(self):
        b = """[i for i in 1, 2 if i]"""
        a = """[i for i in (1, 2) if i]"""
        self.check(b, a)

    def test_4(self):
        b = """[i for i in 1,    2    ]"""
        a = """[i for i in (1,    2)    ]"""
        self.check(b, a)

    def test_5(self):
        b = """(i for i in 1, 2)"""
        a = """(i for i in (1, 2))"""
        self.check(b, a)

    def test_6(self):
        b = """(i for i in 1   ,2   if i)"""
        a = """(i for i in (1   ,2)   if i)"""
        self.check(b, a)

    def test_unchanged_0(self):
        s = """[i for i in (1, 2)]"""
        self.unchanged(s)

    def test_unchanged_1(self):
        s = """[i for i in foo()]"""
        self.unchanged(s)

    def test_unchanged_2(self):
        s = """[i for i in (1, 2) if nothing]"""
        self.unchanged(s)

    def test_unchanged_3(self):
        s = """(i for i in (1, 2))"""
        self.unchanged(s)

    def test_unchanged_4(self):
        s = """[i for i in m]"""
        self.unchanged(s)
