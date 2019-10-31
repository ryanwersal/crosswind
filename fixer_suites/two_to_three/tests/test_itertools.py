from crosswind.tests.support import FixerTestCase


class Test_itertools(FixerTestCase):
    fixer = "itertools"

    def checkall(self, before, after):
        # Because we need to check with and without the itertools prefix
        # and on each of the three functions, these loops make it all
        # much easier
        for i in ("itertools.", ""):
            for f in ("map", "filter", "zip"):
                b = before % (i + "i" + f)
                a = after % (f)
                self.check(b, a)

    def test_0(self):
        # A simple example -- test_1 covers exactly the same thing,
        # but it's not quite as clear.
        b = "itertools.izip(a, b)"
        a = "zip(a, b)"
        self.check(b, a)

    def test_1(self):
        b = """%s(f, a)"""
        a = """%s(f, a)"""
        self.checkall(b, a)

    def test_qualified(self):
        b = """itertools.ifilterfalse(a, b)"""
        a = """itertools.filterfalse(a, b)"""
        self.check(b, a)

        b = """itertools.izip_longest(a, b)"""
        a = """itertools.zip_longest(a, b)"""
        self.check(b, a)

    def test_2(self):
        b = """ifilterfalse(a, b)"""
        a = """filterfalse(a, b)"""
        self.check(b, a)

        b = """izip_longest(a, b)"""
        a = """zip_longest(a, b)"""
        self.check(b, a)

    def test_space_1(self):
        b = """    %s(f, a)"""
        a = """    %s(f, a)"""
        self.checkall(b, a)

    def test_space_2(self):
        b = """    itertools.ifilterfalse(a, b)"""
        a = """    itertools.filterfalse(a, b)"""
        self.check(b, a)

        b = """    itertools.izip_longest(a, b)"""
        a = """    itertools.zip_longest(a, b)"""
        self.check(b, a)

    def test_run_order(self):
        self.assert_runs_after("map", "zip", "filter")
