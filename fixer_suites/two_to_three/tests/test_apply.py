import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(two_to_three_test_case):
    return two_to_three_test_case("apply")


def test_1(fixer):
    b = """x = apply(f, g + h)"""
    a = """x = f(*g + h)"""
    fixer.check(b, a)


def test_2(fixer):
    b = """y = apply(f, g, h)"""
    a = """y = f(*g, **h)"""
    fixer.check(b, a)


def test_3(fixer):
    b = """z = apply(fs[0], g or h, h or g)"""
    a = """z = fs[0](*g or h, **h or g)"""
    fixer.check(b, a)


def test_4(fixer):
    b = """apply(f, (x, y) + t)"""
    a = """f(*(x, y) + t)"""
    fixer.check(b, a)


def test_5(fixer):
    b = """apply(f, args,)"""
    a = """f(*args)"""
    fixer.check(b, a)


def test_6(fixer):
    b = """apply(f, args, kwds,)"""
    a = """f(*args, **kwds)"""
    fixer.check(b, a)


# Test that complex functions are parenthesized


def test_complex_1(fixer):
    b = """x = apply(f+g, args)"""
    a = """x = (f+g)(*args)"""
    fixer.check(b, a)


def test_complex_2(fixer):
    b = """x = apply(f*g, args)"""
    a = """x = (f*g)(*args)"""
    fixer.check(b, a)


def test_complex_3(fixer):
    b = """x = apply(f**g, args)"""
    a = """x = (f**g)(*args)"""
    fixer.check(b, a)


# But dotted names etc. not


def test_dotted_name(fixer):
    b = """x = apply(f.g, args)"""
    a = """x = f.g(*args)"""
    fixer.check(b, a)


def test_subscript(fixer):
    b = """x = apply(f[x], args)"""
    a = """x = f[x](*args)"""
    fixer.check(b, a)


def test_call(fixer):
    b = """x = apply(f(), args)"""
    a = """x = f()(*args)"""
    fixer.check(b, a)


# Extreme case
def test_extreme(fixer):
    b = """x = apply(a.b.c.d.e.f, args, kwds)"""
    a = """x = a.b.c.d.e.f(*args, **kwds)"""
    fixer.check(b, a)


# XXX Comments in weird places still get lost
def test_weird_comments(fixer):
    b = """apply(   # foo
        f, # bar
        args)"""
    a = """f(*args)"""
    fixer.check(b, a)


# These should *not* be touched


def test_unchanged_1(fixer):
    s = """apply()"""
    fixer.unchanged(s)


def test_unchanged_2(fixer):
    s = """apply(f)"""
    fixer.unchanged(s)


def test_unchanged_3(fixer):
    s = """apply(f,)"""
    fixer.unchanged(s)


def test_unchanged_4(fixer):
    s = """apply(f, args, kwds, extras)"""
    fixer.unchanged(s)


def test_unchanged_5(fixer):
    s = """apply(f, *args, **kwds)"""
    fixer.unchanged(s)


def test_unchanged_6(fixer):
    s = """apply(f, *args)"""
    fixer.unchanged(s)


def test_unchanged_6b(fixer):
    s = """apply(f, **kwds)"""
    fixer.unchanged(s)


def test_unchanged_7(fixer):
    s = """apply(func=f, args=args, kwds=kwds)"""
    fixer.unchanged(s)


def test_unchanged_8(fixer):
    s = """apply(f, args=args, kwds=kwds)"""
    fixer.unchanged(s)


def test_unchanged_9(fixer):
    s = """apply(f, args, kwds=kwds)"""
    fixer.unchanged(s)


def test_space_1(fixer):
    a = """apply(  f,  args,   kwds)"""
    b = """f(*args, **kwds)"""
    fixer.check(a, b)


def test_space_2(fixer):
    a = """apply(  f  ,args,kwds   )"""
    b = """f(*args, **kwds)"""
    fixer.check(a, b)
