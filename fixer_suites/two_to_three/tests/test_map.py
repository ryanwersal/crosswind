import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(two_to_three_test_case):
    return two_to_three_test_case("map")


def check(fixer, b, a):
    fixer.unchanged("from future_builtins import map; " + b, a)
    fixer.check(b, a)


def test_prefix_preservation(fixer):
    b = """x =    map(   f,    'abc'   )"""
    a = """x =    list(map(   f,    'abc'   ))"""
    fixer.check(b, a)


def test_map_trailers(fixer):
    b = """x = map(f, 'abc')[0]"""
    a = """x = list(map(f, 'abc'))[0]"""
    fixer.check(b, a)

    b = """x = map(None, l)[0]"""
    a = """x = list(l)[0]"""
    fixer.check(b, a)

    b = """x = map(lambda x:x, l)[0]"""
    a = """x = [x for x in l][0]"""
    fixer.check(b, a)

    b = """x = map(f, 'abc')[0][1]"""
    a = """x = list(map(f, 'abc'))[0][1]"""
    fixer.check(b, a)


def test_trailing_comment(fixer):
    b = """x = map(f, 'abc')   #   foo"""
    a = """x = list(map(f, 'abc'))   #   foo"""
    fixer.check(b, a)


def test_None_with_multiple_arguments(fixer):
    s = """x = map(None, a, b, c)"""
    fixer.warns_unchanged(s, "cannot convert map(None, ...) with multiple arguments")


def test_map_basic(fixer):
    b = """x = map(f, 'abc')"""
    a = """x = list(map(f, 'abc'))"""
    fixer.check(b, a)

    b = """x = len(map(f, 'abc', 'def'))"""
    a = """x = len(list(map(f, 'abc', 'def')))"""
    fixer.check(b, a)

    b = """x = map(None, 'abc')"""
    a = """x = list('abc')"""
    fixer.check(b, a)

    b = """x = map(lambda x: x+1, range(4))"""
    a = """x = [x+1 for x in range(4)]"""
    fixer.check(b, a)

    # Note the parens around x
    b = """x = map(lambda (x): x+1, range(4))"""
    a = """x = [x+1 for x in range(4)]"""
    fixer.check(b, a)

    b = """
        foo()
        # foo
        map(f, x)
        """
    a = """
        foo()
        # foo
        list(map(f, x))
        """
    fixer.warns(b, a, "You should use a for loop here")


def test_map_nochange(fixer):
    a = """b.join(map(f, 'abc'))"""
    fixer.unchanged(a)
    a = """(a + foo(5)).join(map(f, 'abc'))"""
    fixer.unchanged(a)
    a = """iter(map(f, 'abc'))"""
    fixer.unchanged(a)
    a = """list(map(f, 'abc'))"""
    fixer.unchanged(a)
    a = """list(map(f, 'abc'))[0]"""
    fixer.unchanged(a)
    a = """set(map(f, 'abc'))"""
    fixer.unchanged(a)
    a = """set(map(f, 'abc')).pop()"""
    fixer.unchanged(a)
    a = """tuple(map(f, 'abc'))"""
    fixer.unchanged(a)
    a = """any(map(f, 'abc'))"""
    fixer.unchanged(a)
    a = """all(map(f, 'abc'))"""
    fixer.unchanged(a)
    a = """sum(map(f, 'abc'))"""
    fixer.unchanged(a)
    a = """sorted(map(f, 'abc'))"""
    fixer.unchanged(a)
    a = """sorted(map(f, 'abc'), key=blah)"""
    fixer.unchanged(a)
    a = """sorted(map(f, 'abc'), key=blah)[0]"""
    fixer.unchanged(a)
    a = """enumerate(map(f, 'abc'))"""
    fixer.unchanged(a)
    a = """enumerate(map(f, 'abc'), start=1)"""
    fixer.unchanged(a)
    a = """for i in map(f, 'abc'): pass"""
    fixer.unchanged(a)
    a = """[x for x in map(f, 'abc')]"""
    fixer.unchanged(a)
    a = """(x for x in map(f, 'abc'))"""
    fixer.unchanged(a)


def test_future_builtins(fixer):
    a = "from future_builtins import spam, map, eggs; map(f, 'ham')"
    fixer.unchanged(a)

    b = """from future_builtins import spam, eggs; x = map(f, 'abc')"""
    a = """from future_builtins import spam, eggs; x = list(map(f, 'abc'))"""
    fixer.check(b, a)

    a = "from future_builtins import *; map(f, 'ham')"
    fixer.unchanged(a)
