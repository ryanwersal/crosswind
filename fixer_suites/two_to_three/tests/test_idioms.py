import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(two_to_three_test_case):
    return two_to_three_test_case("idioms")


def test_while(fixer):
    b = """while 1: foo()"""
    a = """while True: foo()"""
    fixer.check(b, a)

    b = """while   1: foo()"""
    a = """while   True: foo()"""
    fixer.check(b, a)

    b = """
        while 1:
            foo()
        """
    a = """
        while True:
            foo()
        """
    fixer.check(b, a)


def test_while_unchanged(fixer):
    s = """while 11: foo()"""
    fixer.unchanged(s)

    s = """while 0: foo()"""
    fixer.unchanged(s)

    s = """while foo(): foo()"""
    fixer.unchanged(s)

    s = """while []: foo()"""
    fixer.unchanged(s)


def test_eq_simple(fixer):
    b = """type(x) == T"""
    a = """isinstance(x, T)"""
    fixer.check(b, a)

    b = """if   type(x) == T: pass"""
    a = """if   isinstance(x, T): pass"""
    fixer.check(b, a)


def test_eq_reverse(fixer):
    b = """T == type(x)"""
    a = """isinstance(x, T)"""
    fixer.check(b, a)

    b = """if   T == type(x): pass"""
    a = """if   isinstance(x, T): pass"""
    fixer.check(b, a)


def test_eq_expression(fixer):
    b = """type(x+y) == d.get('T')"""
    a = """isinstance(x+y, d.get('T'))"""
    fixer.check(b, a)

    b = """type(   x  +  y) == d.get('T')"""
    a = """isinstance(x  +  y, d.get('T'))"""
    fixer.check(b, a)


def test_is_simple(fixer):
    b = """type(x) is T"""
    a = """isinstance(x, T)"""
    fixer.check(b, a)

    b = """if   type(x) is T: pass"""
    a = """if   isinstance(x, T): pass"""
    fixer.check(b, a)


def test_is_reverse(fixer):
    b = """T is type(x)"""
    a = """isinstance(x, T)"""
    fixer.check(b, a)

    b = """if   T is type(x): pass"""
    a = """if   isinstance(x, T): pass"""
    fixer.check(b, a)


def test_is_expression(fixer):
    b = """type(x+y) is d.get('T')"""
    a = """isinstance(x+y, d.get('T'))"""
    fixer.check(b, a)

    b = """type(   x  +  y) is d.get('T')"""
    a = """isinstance(x  +  y, d.get('T'))"""
    fixer.check(b, a)


def test_is_not_simple(fixer):
    b = """type(x) is not T"""
    a = """not isinstance(x, T)"""
    fixer.check(b, a)

    b = """if   type(x) is not T: pass"""
    a = """if   not isinstance(x, T): pass"""
    fixer.check(b, a)


def test_is_not_reverse(fixer):
    b = """T is not type(x)"""
    a = """not isinstance(x, T)"""
    fixer.check(b, a)

    b = """if   T is not type(x): pass"""
    a = """if   not isinstance(x, T): pass"""
    fixer.check(b, a)


def test_is_not_expression(fixer):
    b = """type(x+y) is not d.get('T')"""
    a = """not isinstance(x+y, d.get('T'))"""
    fixer.check(b, a)

    b = """type(   x  +  y) is not d.get('T')"""
    a = """not isinstance(x  +  y, d.get('T'))"""
    fixer.check(b, a)


def test_ne_simple(fixer):
    b = """type(x) != T"""
    a = """not isinstance(x, T)"""
    fixer.check(b, a)

    b = """if   type(x) != T: pass"""
    a = """if   not isinstance(x, T): pass"""
    fixer.check(b, a)


def test_ne_reverse(fixer):
    b = """T != type(x)"""
    a = """not isinstance(x, T)"""
    fixer.check(b, a)

    b = """if   T != type(x): pass"""
    a = """if   not isinstance(x, T): pass"""
    fixer.check(b, a)


def test_ne_expression(fixer):
    b = """type(x+y) != d.get('T')"""
    a = """not isinstance(x+y, d.get('T'))"""
    fixer.check(b, a)

    b = """type(   x  +  y) != d.get('T')"""
    a = """not isinstance(x  +  y, d.get('T'))"""
    fixer.check(b, a)


def test_type_unchanged(fixer):
    a = """type(x).__name__"""
    fixer.unchanged(a)


def test_sort_list_call(fixer):
    b = """
        v = list(t)
        v.sort()
        foo(v)
        """
    a = """
        v = sorted(t)
        foo(v)
        """
    fixer.check(b, a)

    b = """
        v = list(foo(b) + d)
        v.sort()
        foo(v)
        """
    a = """
        v = sorted(foo(b) + d)
        foo(v)
        """
    fixer.check(b, a)

    b = """
        while x:
            v = list(t)
            v.sort()
            foo(v)
        """
    a = """
        while x:
            v = sorted(t)
            foo(v)
        """
    fixer.check(b, a)

    b = """
        v = list(t)
        # foo
        v.sort()
        foo(v)
        """
    a = """
        v = sorted(t)
        # foo
        foo(v)
        """
    fixer.check(b, a)

    b = r"""
        v = list(   t)
        v.sort()
        foo(v)
        """
    a = r"""
        v = sorted(   t)
        foo(v)
        """
    fixer.check(b, a)

    b = r"""
        try:
            m = list(s)
            m.sort()
        except: pass
        """

    a = r"""
        try:
            m = sorted(s)
        except: pass
        """
    fixer.check(b, a)

    b = r"""
        try:
            m = list(s)
            # foo
            m.sort()
        except: pass
        """

    a = r"""
        try:
            m = sorted(s)
            # foo
        except: pass
        """
    fixer.check(b, a)

    b = r"""
        m = list(s)
        # more comments
        m.sort()"""

    a = r"""
        m = sorted(s)
        # more comments"""
    fixer.check(b, a)


def test_sort_simple_expr(fixer):
    b = """
        v = t
        v.sort()
        foo(v)
        """
    a = """
        v = sorted(t)
        foo(v)
        """
    fixer.check(b, a)

    b = """
        v = foo(b)
        v.sort()
        foo(v)
        """
    a = """
        v = sorted(foo(b))
        foo(v)
        """
    fixer.check(b, a)

    b = """
        v = b.keys()
        v.sort()
        foo(v)
        """
    a = """
        v = sorted(b.keys())
        foo(v)
        """
    fixer.check(b, a)

    b = """
        v = foo(b) + d
        v.sort()
        foo(v)
        """
    a = """
        v = sorted(foo(b) + d)
        foo(v)
        """
    fixer.check(b, a)

    b = """
        while x:
            v = t
            v.sort()
            foo(v)
        """
    a = """
        while x:
            v = sorted(t)
            foo(v)
        """
    fixer.check(b, a)

    b = """
        v = t
        # foo
        v.sort()
        foo(v)
        """
    a = """
        v = sorted(t)
        # foo
        foo(v)
        """
    fixer.check(b, a)

    b = r"""
        v =   t
        v.sort()
        foo(v)
        """
    a = r"""
        v =   sorted(t)
        foo(v)
        """
    fixer.check(b, a)


def test_sort_unchanged(fixer):
    s = """
        v = list(t)
        w.sort()
        foo(w)
        """
    fixer.unchanged(s)

    s = """
        v = list(t)
        v.sort(u)
        foo(v)
        """
    fixer.unchanged(s)
