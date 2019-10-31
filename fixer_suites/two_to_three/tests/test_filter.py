import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(two_to_three_test_case):
    return two_to_three_test_case("filter")


def test_prefix_preservation(fixer):
    b = """x =   filter(    foo,     'abc'   )"""
    a = """x =   list(filter(    foo,     'abc'   ))"""
    fixer.check(b, a)

    b = """x =   filter(  None , 'abc'  )"""
    a = """x =   [_f for _f in 'abc' if _f]"""
    fixer.check(b, a)


def test_filter_basic(fixer):
    b = """x = filter(None, 'abc')"""
    a = """x = [_f for _f in 'abc' if _f]"""
    fixer.check(b, a)

    b = """x = len(filter(f, 'abc'))"""
    a = """x = len(list(filter(f, 'abc')))"""
    fixer.check(b, a)

    b = """x = filter(lambda x: x%2 == 0, range(10))"""
    a = """x = [x for x in range(10) if x%2 == 0]"""
    fixer.check(b, a)

    # Note the parens around x
    b = """x = filter(lambda (x): x%2 == 0, range(10))"""
    a = """x = [x for x in range(10) if x%2 == 0]"""
    fixer.check(b, a)


def test_filter_trailers(fixer):
    b = """x = filter(None, 'abc')[0]"""
    a = """x = [_f for _f in 'abc' if _f][0]"""
    fixer.check(b, a)

    b = """x = len(filter(f, 'abc')[0])"""
    a = """x = len(list(filter(f, 'abc'))[0])"""
    fixer.check(b, a)

    b = """x = filter(lambda x: x%2 == 0, range(10))[0]"""
    a = """x = [x for x in range(10) if x%2 == 0][0]"""
    fixer.check(b, a)

    # Note the parens around x
    b = """x = filter(lambda (x): x%2 == 0, range(10))[0]"""
    a = """x = [x for x in range(10) if x%2 == 0][0]"""
    fixer.check(b, a)


def test_filter_nochange(fixer):
    a = """b.join(filter(f, 'abc'))"""
    fixer.unchanged(a)
    a = """(a + foo(5)).join(filter(f, 'abc'))"""
    fixer.unchanged(a)
    a = """iter(filter(f, 'abc'))"""
    fixer.unchanged(a)
    a = """list(filter(f, 'abc'))"""
    fixer.unchanged(a)
    a = """list(filter(f, 'abc'))[0]"""
    fixer.unchanged(a)
    a = """set(filter(f, 'abc'))"""
    fixer.unchanged(a)
    a = """set(filter(f, 'abc')).pop()"""
    fixer.unchanged(a)
    a = """tuple(filter(f, 'abc'))"""
    fixer.unchanged(a)
    a = """any(filter(f, 'abc'))"""
    fixer.unchanged(a)
    a = """all(filter(f, 'abc'))"""
    fixer.unchanged(a)
    a = """sum(filter(f, 'abc'))"""
    fixer.unchanged(a)
    a = """sorted(filter(f, 'abc'))"""
    fixer.unchanged(a)
    a = """sorted(filter(f, 'abc'), key=blah)"""
    fixer.unchanged(a)
    a = """sorted(filter(f, 'abc'), key=blah)[0]"""
    fixer.unchanged(a)
    a = """enumerate(filter(f, 'abc'))"""
    fixer.unchanged(a)
    a = """enumerate(filter(f, 'abc'), start=1)"""
    fixer.unchanged(a)
    a = """for i in filter(f, 'abc'): pass"""
    fixer.unchanged(a)
    a = """[x for x in filter(f, 'abc')]"""
    fixer.unchanged(a)
    a = """(x for x in filter(f, 'abc'))"""
    fixer.unchanged(a)


def test_future_builtins(fixer):
    a = "from future_builtins import spam, filter; filter(f, 'ham')"
    fixer.unchanged(a)

    b = """from future_builtins import spam; x = filter(f, 'abc')"""
    a = """from future_builtins import spam; x = list(filter(f, 'abc'))"""
    fixer.check(b, a)

    a = "from future_builtins import *; filter(f, 'ham')"
    fixer.unchanged(a)
