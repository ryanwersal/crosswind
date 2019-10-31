import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(three_to_two_test_case):
    return three_to_two_test_case("next")


def test_1(fixer):
    b = """next(it)"""
    a = """it.next()"""
    fixer.check(b, a)


def test_2(fixer):
    b = """next(a.b.c.d)"""
    a = """a.b.c.d.next()"""
    fixer.check(b, a)


def test_3(fixer):
    b = """next((a + b))"""
    a = """(a + b).next()"""
    fixer.check(b, a)


def test_4(fixer):
    b = """next(a())"""
    a = """a().next()"""
    fixer.check(b, a)


def test_5(fixer):
    b = """next(a()) + b"""
    a = """a().next() + b"""
    fixer.check(b, a)


def test_6(fixer):
    b = """c(      next(a()) + b)"""
    a = """c(      a().next() + b)"""
    fixer.check(b, a)


def test_prefix_preservation_1(fixer):
    b = """
        for a in b:
            foo(a)
            next(a)
        """
    a = """
        for a in b:
            foo(a)
            a.next()
        """
    fixer.check(b, a)


def test_prefix_preservation_2(fixer):
    b = """
        for a in b:
            foo(a) # abc
            # def
            next(a)
        """
    a = """
        for a in b:
            foo(a) # abc
            # def
            a.next()
        """
    fixer.check(b, a)


def test_prefix_preservation_3(fixer):
    b = """
        next = 5
        for a in b:
            foo(a)
            a.__next__()
        """

    a = """
        next = 5
        for a in b:
            foo(a)
            a.next()
        """
    fixer.check(b, a)


def test_prefix_preservation_4(fixer):
    b = """
        next = 5
        for a in b:
            foo(a) # abc
            # def
            a.__next__()
        """
    a = """
        next = 5
        for a in b:
            foo(a) # abc
            # def
            a.next()
        """
    fixer.check(b, a)


def test_prefix_preservation_5(fixer):
    b = """
        next = 5
        for a in b:
            foo(foo(a), # abc
                a.__next__())
        """
    a = """
        next = 5
        for a in b:
            foo(foo(a), # abc
                a.next())
        """
    fixer.check(b, a)


def test_prefix_preservation_6(fixer):
    b = """
        for a in b:
            foo(foo(a), # abc
                next(a))
        """
    a = """
        for a in b:
            foo(foo(a), # abc
                a.next())
        """
    fixer.check(b, a)


def test_method_1(fixer):
    b = """
        class A:
            def __next__(self):
                pass
        """
    a = """
        class A:
            def next(self):
                pass
        """
    fixer.check(b, a)


def test_method_2(fixer):
    b = """
        class A(object):
            def __next__(self):
                pass
        """
    a = """
        class A(object):
            def next(self):
                pass
        """
    fixer.check(b, a)


def test_method_3(fixer):
    b = """
        class A:
            def __next__(x):
                pass
        """
    a = """
        class A:
            def next(x):
                pass
        """
    fixer.check(b, a)


def test_method_4(fixer):
    b = """
        class A:
            def __init__(self, foo):
                self.foo = foo

            def __next__(self):
                pass

            def __iter__(self):
                return self
        """
    a = """
        class A:
            def __init__(self, foo):
                self.foo = foo

            def next(self):
                pass

            def __iter__(self):
                return self
        """
    fixer.check(b, a)


def test_noncall_access_1(fixer):
    b = """gnext = g.__next__"""
    a = """gnext = g.next"""
    fixer.check(b, a)


def test_noncall_access_2(fixer):
    b = """f(g.__next__ + 5)"""
    a = """f(g.next + 5)"""
    fixer.check(b, a)


def test_noncall_access_3(fixer):
    b = """f(g().__next__ + 5)"""
    a = """f(g().next + 5)"""
    fixer.check(b, a)
