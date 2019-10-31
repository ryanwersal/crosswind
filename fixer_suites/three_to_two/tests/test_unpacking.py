import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(three_to_two_test_case):
    return three_to_two_test_case("unpacking")


def test_unchanged(fixer):
    s = "def f(*args): pass"
    fixer.unchanged(s)

    s = "for i in range(s): pass"
    fixer.unchanged(s)

    s = "a, b, c = range(100)"
    fixer.unchanged(s)


def test_forloop(fixer):
    b = """
    for a, b, c, *d, e in two_dim_array: pass"""
    a = """
    for _crosswinditer in two_dim_array:
        _crosswindlist = list(_crosswinditer)
        a, b, c, d, e, = _crosswindlist[:3] + [_crosswindlist[3:-1]] + _crosswindlist[-1:]
        pass"""
    fixer.check(b, a)

    b = """
    for a, b, *c in some_thing:
        do_stuff"""
    a = """
    for _crosswinditer in some_thing:
        _crosswindlist = list(_crosswinditer)
        a, b, c, = _crosswindlist[:2] + [_crosswindlist[2:]]
        do_stuff"""
    fixer.check(b, a)

    b = """
    for *a, b, c, d, e, f, g in some_thing:
        pass"""
    a = """
    for _crosswinditer in some_thing:
        _crosswindlist = list(_crosswinditer)
        a, b, c, d, e, f, g, = [_crosswindlist[:-6]] + _crosswindlist[-6:]
        pass"""
    fixer.check(b, a)


def test_assignment(fixer):
    b = """
    a, *b, c = range(100)"""
    a = """
    _crosswindlist = list(range(100))
    a, b, c, = _crosswindlist[:1] + [_crosswindlist[1:-1]] + _crosswindlist[-1:]"""
    fixer.check(b, a)

    b = """
    a, b, c, d, *e, f, g = letters"""
    a = """
    _crosswindlist = list(letters)
    a, b, c, d, e, f, g, = _crosswindlist[:4] + [_crosswindlist[4:-2]] + _crosswindlist[-2:]"""
    fixer.check(b, a)

    b = """
    *e, f, g = letters"""
    a = """
    _crosswindlist = list(letters)
    e, f, g, = [_crosswindlist[:-2]] + _crosswindlist[-2:]"""
    fixer.check(b, a)

    b = """
    a, b, c, d, *e = stuff"""
    a = """
    _crosswindlist = list(stuff)
    a, b, c, d, e, = _crosswindlist[:4] + [_crosswindlist[4:]]"""
    fixer.check(b, a)

    b = """
    *z, = stuff"""
    a = """
    _crosswindlist = list(stuff)
    z, = [_crosswindlist[:]]"""
    fixer.check(b, a)

    b = """
    while True:
        a, *b, c = stuff
        other_stuff = make_more_stuff(a, b, c)"""

    a = """
    while True:
        _crosswindlist = list(stuff)
        a, b, c, = _crosswindlist[:1] + [_crosswindlist[1:-1]] + _crosswindlist[-1:]
        other_stuff = make_more_stuff(a, b, c)"""
    fixer.check(b, a)
