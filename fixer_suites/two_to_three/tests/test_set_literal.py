import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(two_to_three_test_case):
    return two_to_three_test_case("set_literal")


def test_basic(fixer):
    b = """set([1, 2, 3])"""
    a = """{1, 2, 3}"""
    fixer.check(b, a)

    b = """set((1, 2, 3))"""
    a = """{1, 2, 3}"""
    fixer.check(b, a)

    b = """set((1,))"""
    a = """{1}"""
    fixer.check(b, a)

    b = """set([1])"""
    fixer.check(b, a)

    b = """set((a, b))"""
    a = """{a, b}"""
    fixer.check(b, a)

    b = """set([a, b])"""
    fixer.check(b, a)

    b = """set((a*234, f(args=23)))"""
    a = """{a*234, f(args=23)}"""
    fixer.check(b, a)

    b = """set([a*23, f(23)])"""
    a = """{a*23, f(23)}"""
    fixer.check(b, a)

    b = """set([a-234**23])"""
    a = """{a-234**23}"""
    fixer.check(b, a)


def test_listcomps(fixer):
    b = """set([x for x in y])"""
    a = """{x for x in y}"""
    fixer.check(b, a)

    b = """set([x for x in y if x == m])"""
    a = """{x for x in y if x == m}"""
    fixer.check(b, a)

    b = """set([x for x in y for a in b])"""
    a = """{x for x in y for a in b}"""
    fixer.check(b, a)

    b = """set([f(x) - 23 for x in y])"""
    a = """{f(x) - 23 for x in y}"""
    fixer.check(b, a)


def test_whitespace(fixer):
    b = """set( [1, 2])"""
    a = """{1, 2}"""
    fixer.check(b, a)

    b = """set([1 ,  2])"""
    a = """{1 ,  2}"""
    fixer.check(b, a)

    b = """set([ 1 ])"""
    a = """{ 1 }"""
    fixer.check(b, a)

    b = """set( [1] )"""
    a = """{1}"""
    fixer.check(b, a)

    b = """set([  1,  2  ])"""
    a = """{  1,  2  }"""
    fixer.check(b, a)

    b = """set([x  for x in y ])"""
    a = """{x  for x in y }"""
    fixer.check(b, a)

    b = """set(
                [1, 2]
            )
        """
    a = """{1, 2}\n"""
    fixer.check(b, a)


def test_comments(fixer):
    b = """set((1, 2)) # Hi"""
    a = """{1, 2} # Hi"""
    fixer.check(b, a)

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
    fixer.check(b, a)


def test_unchanged(fixer):
    s = """set()"""
    fixer.unchanged(s)

    s = """set(a)"""
    fixer.unchanged(s)

    s = """set(a, b, c)"""
    fixer.unchanged(s)

    # Don't transform generators because they might have to be lazy.
    s = """set(x for x in y)"""
    fixer.unchanged(s)

    s = """set(x for x in y if z)"""
    fixer.unchanged(s)

    s = """set(a*823-23**2 + f(23))"""
    fixer.unchanged(s)
