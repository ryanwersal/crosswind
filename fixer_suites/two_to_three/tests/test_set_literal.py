from .util import FixerTestCase


class Test_set_literal(FixerTestCase):

    fixer = "set_literal"

    def test_basic(self):
        b = """set([1, 2, 3])"""
        a = """{1, 2, 3}"""
        self.check(b, a)

        b = """set((1, 2, 3))"""
        a = """{1, 2, 3}"""
        self.check(b, a)

        b = """set((1,))"""
        a = """{1}"""
        self.check(b, a)

        b = """set([1])"""
        self.check(b, a)

        b = """set((a, b))"""
        a = """{a, b}"""
        self.check(b, a)

        b = """set([a, b])"""
        self.check(b, a)

        b = """set((a*234, f(args=23)))"""
        a = """{a*234, f(args=23)}"""
        self.check(b, a)

        b = """set([a*23, f(23)])"""
        a = """{a*23, f(23)}"""
        self.check(b, a)

        b = """set([a-234**23])"""
        a = """{a-234**23}"""
        self.check(b, a)

    def test_listcomps(self):
        b = """set([x for x in y])"""
        a = """{x for x in y}"""
        self.check(b, a)

        b = """set([x for x in y if x == m])"""
        a = """{x for x in y if x == m}"""
        self.check(b, a)

        b = """set([x for x in y for a in b])"""
        a = """{x for x in y for a in b}"""
        self.check(b, a)

        b = """set([f(x) - 23 for x in y])"""
        a = """{f(x) - 23 for x in y}"""
        self.check(b, a)

    def test_whitespace(self):
        b = """set( [1, 2])"""
        a = """{1, 2}"""
        self.check(b, a)

        b = """set([1 ,  2])"""
        a = """{1 ,  2}"""
        self.check(b, a)

        b = """set([ 1 ])"""
        a = """{ 1 }"""
        self.check(b, a)

        b = """set( [1] )"""
        a = """{1}"""
        self.check(b, a)

        b = """set([  1,  2  ])"""
        a = """{  1,  2  }"""
        self.check(b, a)

        b = """set([x  for x in y ])"""
        a = """{x  for x in y }"""
        self.check(b, a)

        b = """set(
                   [1, 2]
               )
            """
        a = """{1, 2}\n"""
        self.check(b, a)

    def test_comments(self):
        b = """set((1, 2)) # Hi"""
        a = """{1, 2} # Hi"""
        self.check(b, a)

        # This isn't optimal behavior, but the fixer is optional.
        b = """
            # Foo
            set( # Bar
               (1, 2)
            )
            """
        a = """
            # Foo
            {1, 2}
            """
        self.check(b, a)

    def test_unchanged(self):
        s = """set()"""
        self.unchanged(s)

        s = """set(a)"""
        self.unchanged(s)

        s = """set(a, b, c)"""
        self.unchanged(s)

        # Don't transform generators because they might have to be lazy.
        s = """set(x for x in y)"""
        self.unchanged(s)

        s = """set(x for x in y if z)"""
        self.unchanged(s)

        s = """set(a*823-23**2 + f(23))"""
        self.unchanged(s)
