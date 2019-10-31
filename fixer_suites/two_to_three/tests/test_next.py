import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(two_to_three_test_case):
    return two_to_three_test_case("next")


def test_1(fixer):
    b = """it.next()"""
    a = """next(it)"""
    fixer.check(b, a)


def test_2(fixer):
    b = """a.b.c.d.next()"""
    a = """next(a.b.c.d)"""
    fixer.check(b, a)


def test_3(fixer):
    b = """(a + b).next()"""
    a = """next((a + b))"""
    fixer.check(b, a)


def test_4(fixer):
    b = """a().next()"""
    a = """next(a())"""
    fixer.check(b, a)


def test_5(fixer):
    b = """a().next() + b"""
    a = """next(a()) + b"""
    fixer.check(b, a)


def test_6(fixer):
    b = """c(      a().next() + b)"""
    a = """c(      next(a()) + b)"""
    fixer.check(b, a)


def test_prefix_preservation_1(fixer):
    b = """
        for a in b:
            foo(a)
            a.next()
        """
    a = """
        for a in b:
            foo(a)
            next(a)
        """
    fixer.check(b, a)


def test_prefix_preservation_2(fixer):
    b = """
        for a in b:
            foo(a) # abc
            # def
            a.next()
        """
    a = """
        for a in b:
            foo(a) # abc
            # def
            next(a)
        """
    fixer.check(b, a)


def test_prefix_preservation_3(fixer):
    b = """
        next = 5
        for a in b:
            foo(a)
            a.next()
        """
    a = """
        next = 5
        for a in b:
            foo(a)
            a.__next__()
        """
    fixer.check(b, a, ignore_warnings=True)


def test_prefix_preservation_4(fixer):
    b = """
        next = 5
        for a in b:
            foo(a) # abc
            # def
            a.next()
        """
    a = """
        next = 5
        for a in b:
            foo(a) # abc
            # def
            a.__next__()
        """
    fixer.check(b, a, ignore_warnings=True)


def test_prefix_preservation_5(fixer):
    b = """
        next = 5
        for a in b:
            foo(foo(a), # abc
                a.next())
        """
    a = """
        next = 5
        for a in b:
            foo(foo(a), # abc
                a.__next__())
        """
    fixer.check(b, a, ignore_warnings=True)


def test_prefix_preservation_6(fixer):
    b = """
        for a in b:
            foo(foo(a), # abc
                a.next())
        """
    a = """
        for a in b:
            foo(foo(a), # abc
                next(a))
        """
    fixer.check(b, a)


def test_method_1(fixer):
    b = """
        class A:
            def next(self):
                pass
        """
    a = """
        class A:
            def __next__(self):
                pass
        """
    fixer.check(b, a)


def test_method_2(fixer):
    b = """
        class A(object):
            def next(self):
                pass
        """
    a = """
        class A(object):
            def __next__(self):
                pass
        """
    fixer.check(b, a)


def test_method_3(fixer):
    b = """
        class A:
            def next(x):
                pass
        """
    a = """
        class A:
            def __next__(x):
                pass
        """
    fixer.check(b, a)


def test_method_4(fixer):
    b = """
        class A:
            def __init__(self, foo):
                self.foo = foo

            def next(self):
                pass

            def __iter__(self):
                return self
        """
    a = """
        class A:
            def __init__(self, foo):
                self.foo = foo

            def __next__(self):
                pass

            def __iter__(self):
                return self
        """
    fixer.check(b, a)


def test_method_unchanged(fixer):
    s = """
        class A:
            def next(self, a, b):
                pass
        """
    fixer.unchanged(s)


def test_shadowing_assign_simple(fixer):
    s = """
        next = foo

        class A:
            def next(self, a, b):
                pass
        """
    fixer.warns_unchanged(s, "Calls to builtin next() possibly shadowed")


def test_shadowing_assign_tuple_1(fixer):
    s = """
        (next, a) = foo

        class A:
            def next(self, a, b):
                pass
        """
    fixer.warns_unchanged(s, "Calls to builtin next() possibly shadowed")


def test_shadowing_assign_tuple_2(fixer):
    s = """
        (a, (b, (next, c)), a) = foo

        class A:
            def next(self, a, b):
                pass
        """
    fixer.warns_unchanged(s, "Calls to builtin next() possibly shadowed")


def test_shadowing_assign_list_1(fixer):
    s = """
        [next, a] = foo

        class A:
            def next(self, a, b):
                pass
        """
    fixer.warns_unchanged(s, "Calls to builtin next() possibly shadowed")


def test_shadowing_assign_list_2(fixer):
    s = """
        [a, [b, [next, c]], a] = foo

        class A:
            def next(self, a, b):
                pass
        """
    fixer.warns_unchanged(s, "Calls to builtin next() possibly shadowed")


def test_builtin_assign(fixer):
    s = """
        def foo():
            __builtin__.next = foo

        class A:
            def next(self, a, b):
                pass
        """
    fixer.warns_unchanged(s, "Calls to builtin next() possibly shadowed")


def test_builtin_assign_in_tuple(fixer):
    s = """
        def foo():
            (a, __builtin__.next) = foo

        class A:
            def next(self, a, b):
                pass
        """
    fixer.warns_unchanged(s, "Calls to builtin next() possibly shadowed")


def test_builtin_assign_in_list(fixer):
    s = """
        def foo():
            [a, __builtin__.next] = foo

        class A:
            def next(self, a, b):
                pass
        """
    fixer.warns_unchanged(s, "Calls to builtin next() possibly shadowed")


def test_assign_to_next(fixer):
    s = """
        def foo():
            A.next = foo

        class A:
            def next(self, a, b):
                pass
        """
    fixer.unchanged(s)


def test_assign_to_next_in_tuple(fixer):
    s = """
        def foo():
            (a, A.next) = foo

        class A:
            def next(self, a, b):
                pass
        """
    fixer.unchanged(s)


def test_assign_to_next_in_list(fixer):
    s = """
        def foo():
            [a, A.next] = foo

        class A:
            def next(self, a, b):
                pass
        """
    fixer.unchanged(s)


def test_shadowing_import_1(fixer):
    s = """
        import foo.bar as next

        class A:
            def next(self, a, b):
                pass
        """
    fixer.warns_unchanged(s, "Calls to builtin next() possibly shadowed")


def test_shadowing_import_2(fixer):
    s = """
        import bar, bar.foo as next

        class A:
            def next(self, a, b):
                pass
        """
    fixer.warns_unchanged(s, "Calls to builtin next() possibly shadowed")


def test_shadowing_import_3(fixer):
    s = """
        import bar, bar.foo as next, baz

        class A:
            def next(self, a, b):
                pass
        """
    fixer.warns_unchanged(s, "Calls to builtin next() possibly shadowed")


def test_shadowing_import_from_1(fixer):
    s = """
        from x import next

        class A:
            def next(self, a, b):
                pass
        """
    fixer.warns_unchanged(s, "Calls to builtin next() possibly shadowed")


def test_shadowing_import_from_2(fixer):
    s = """
        from x.a import next

        class A:
            def next(self, a, b):
                pass
        """
    fixer.warns_unchanged(s, "Calls to builtin next() possibly shadowed")


def test_shadowing_import_from_3(fixer):
    s = """
        from x import a, next, b

        class A:
            def next(self, a, b):
                pass
        """
    fixer.warns_unchanged(s, "Calls to builtin next() possibly shadowed")


def test_shadowing_import_from_4(fixer):
    s = """
        from x.a import a, next, b

        class A:
            def next(self, a, b):
                pass
        """
    fixer.warns_unchanged(s, "Calls to builtin next() possibly shadowed")


def test_shadowing_funcdef_1(fixer):
    s = """
        def next(a):
            pass

        class A:
            def next(self, a, b):
                pass
        """
    fixer.warns_unchanged(s, "Calls to builtin next() possibly shadowed")


def test_shadowing_funcdef_2(fixer):
    b = """
        def next(a):
            pass

        class A:
            def next(self):
                pass

        it.next()
        """
    a = """
        def next(a):
            pass

        class A:
            def __next__(self):
                pass

        it.__next__()
        """
    fixer.warns(b, a, "Calls to builtin next() possibly shadowed")


def test_shadowing_global_1(fixer):
    s = """
        def f():
            global next
            next = 5
        """
    fixer.warns_unchanged(s, "Calls to builtin next() possibly shadowed")


def test_shadowing_global_2(fixer):
    s = """
        def f():
            global a, next, b
            next = 5
        """
    fixer.warns_unchanged(s, "Calls to builtin next() possibly shadowed")


def test_shadowing_for_simple(fixer):
    s = """
        for next in it():
            pass

        b = 5
        c = 6
        """
    fixer.warns_unchanged(s, "Calls to builtin next() possibly shadowed")


def test_shadowing_for_tuple_1(fixer):
    s = """
        for next, b in it():
            pass

        b = 5
        c = 6
        """
    fixer.warns_unchanged(s, "Calls to builtin next() possibly shadowed")


def test_shadowing_for_tuple_2(fixer):
    s = """
        for a, (next, c), b in it():
            pass

        b = 5
        c = 6
        """
    fixer.warns_unchanged(s, "Calls to builtin next() possibly shadowed")


def test_noncall_access_1(fixer):
    b = """gnext = g.next"""
    a = """gnext = g.__next__"""
    fixer.check(b, a)


def test_noncall_access_2(fixer):
    b = """f(g.next + 5)"""
    a = """f(g.__next__ + 5)"""
    fixer.check(b, a)


def test_noncall_access_3(fixer):
    b = """f(g().next + 5)"""
    a = """f(g().__next__ + 5)"""
    fixer.check(b, a)
