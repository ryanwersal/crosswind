from lib3to2.tests.test_all_fixers import lib3to2FixerTestCase

class Test_zip(lib3to2FixerTestCase):
    fixer = "zip"

    def test_zip_basic(self):
        b = """x = zip(a, b, c)"""
        a = """x = list(zip(a, b, c))"""
        self.check(b, a)

        b = """x = len(zip(a, b))"""
        a = """x = len(list(zip(a, b)))"""
        self.check(b, a)

    def test_zip_nochange(self):
        a = """b.join(zip(a, b))"""
        self.unchanged(a)
        a = """(a + foo(5)).join(zip(a, b))"""
        self.unchanged(a)
        a = """iter(zip(a, b))"""
        self.unchanged(a)
        a = """list(zip(a, b))"""
        self.unchanged(a)
        a = """list(zip(a, b))[0]"""
        self.unchanged(a)
        a = """set(zip(a, b))"""
        self.unchanged(a)
        a = """set(zip(a, b)).pop()"""
        self.unchanged(a)
        a = """tuple(zip(a, b))"""
        self.unchanged(a)
        a = """any(zip(a, b))"""
        self.unchanged(a)
        a = """all(zip(a, b))"""
        self.unchanged(a)
        a = """sum(zip(a, b))"""
        self.unchanged(a)
        a = """sorted(zip(a, b))"""
        self.unchanged(a)
        a = """sorted(zip(a, b), key=blah)"""
        self.unchanged(a)
        a = """sorted(zip(a, b), key=blah)[0]"""
        self.unchanged(a)
        a = """for i in zip(a, b): pass"""
        self.unchanged(a)
        a = """[x for x in zip(a, b)]"""
        self.unchanged(a)
        a = """(x for x in zip(a, b))"""
        self.unchanged(a)
