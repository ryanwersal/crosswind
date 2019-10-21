from .util import FixerTestCase


class Test_next(FixerTestCase):
    fixer = "next"

    def test_1(self):
        b = """it.next()"""
        a = """next(it)"""
        self.check(b, a)

    def test_2(self):
        b = """a.b.c.d.next()"""
        a = """next(a.b.c.d)"""
        self.check(b, a)

    def test_3(self):
        b = """(a + b).next()"""
        a = """next((a + b))"""
        self.check(b, a)

    def test_4(self):
        b = """a().next()"""
        a = """next(a())"""
        self.check(b, a)

    def test_5(self):
        b = """a().next() + b"""
        a = """next(a()) + b"""
        self.check(b, a)

    def test_6(self):
        b = """c(      a().next() + b)"""
        a = """c(      next(a()) + b)"""
        self.check(b, a)

    def test_prefix_preservation_1(self):
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
        self.check(b, a)

    def test_prefix_preservation_2(self):
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
        self.check(b, a)

    def test_prefix_preservation_3(self):
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
        self.check(b, a, ignore_warnings=True)

    def test_prefix_preservation_4(self):
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
        self.check(b, a, ignore_warnings=True)

    def test_prefix_preservation_5(self):
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
        self.check(b, a, ignore_warnings=True)

    def test_prefix_preservation_6(self):
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
        self.check(b, a)

    def test_method_1(self):
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
        self.check(b, a)

    def test_method_2(self):
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
        self.check(b, a)

    def test_method_3(self):
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
        self.check(b, a)

    def test_method_4(self):
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
        self.check(b, a)

    def test_method_unchanged(self):
        s = """
            class A:
                def next(self, a, b):
                    pass
            """
        self.unchanged(s)

    def test_shadowing_assign_simple(self):
        s = """
            next = foo

            class A:
                def next(self, a, b):
                    pass
            """
        self.warns_unchanged(s, "Calls to builtin next() possibly shadowed")

    def test_shadowing_assign_tuple_1(self):
        s = """
            (next, a) = foo

            class A:
                def next(self, a, b):
                    pass
            """
        self.warns_unchanged(s, "Calls to builtin next() possibly shadowed")

    def test_shadowing_assign_tuple_2(self):
        s = """
            (a, (b, (next, c)), a) = foo

            class A:
                def next(self, a, b):
                    pass
            """
        self.warns_unchanged(s, "Calls to builtin next() possibly shadowed")

    def test_shadowing_assign_list_1(self):
        s = """
            [next, a] = foo

            class A:
                def next(self, a, b):
                    pass
            """
        self.warns_unchanged(s, "Calls to builtin next() possibly shadowed")

    def test_shadowing_assign_list_2(self):
        s = """
            [a, [b, [next, c]], a] = foo

            class A:
                def next(self, a, b):
                    pass
            """
        self.warns_unchanged(s, "Calls to builtin next() possibly shadowed")

    def test_builtin_assign(self):
        s = """
            def foo():
                __builtin__.next = foo

            class A:
                def next(self, a, b):
                    pass
            """
        self.warns_unchanged(s, "Calls to builtin next() possibly shadowed")

    def test_builtin_assign_in_tuple(self):
        s = """
            def foo():
                (a, __builtin__.next) = foo

            class A:
                def next(self, a, b):
                    pass
            """
        self.warns_unchanged(s, "Calls to builtin next() possibly shadowed")

    def test_builtin_assign_in_list(self):
        s = """
            def foo():
                [a, __builtin__.next] = foo

            class A:
                def next(self, a, b):
                    pass
            """
        self.warns_unchanged(s, "Calls to builtin next() possibly shadowed")

    def test_assign_to_next(self):
        s = """
            def foo():
                A.next = foo

            class A:
                def next(self, a, b):
                    pass
            """
        self.unchanged(s)

    def test_assign_to_next_in_tuple(self):
        s = """
            def foo():
                (a, A.next) = foo

            class A:
                def next(self, a, b):
                    pass
            """
        self.unchanged(s)

    def test_assign_to_next_in_list(self):
        s = """
            def foo():
                [a, A.next] = foo

            class A:
                def next(self, a, b):
                    pass
            """
        self.unchanged(s)

    def test_shadowing_import_1(self):
        s = """
            import foo.bar as next

            class A:
                def next(self, a, b):
                    pass
            """
        self.warns_unchanged(s, "Calls to builtin next() possibly shadowed")

    def test_shadowing_import_2(self):
        s = """
            import bar, bar.foo as next

            class A:
                def next(self, a, b):
                    pass
            """
        self.warns_unchanged(s, "Calls to builtin next() possibly shadowed")

    def test_shadowing_import_3(self):
        s = """
            import bar, bar.foo as next, baz

            class A:
                def next(self, a, b):
                    pass
            """
        self.warns_unchanged(s, "Calls to builtin next() possibly shadowed")

    def test_shadowing_import_from_1(self):
        s = """
            from x import next

            class A:
                def next(self, a, b):
                    pass
            """
        self.warns_unchanged(s, "Calls to builtin next() possibly shadowed")

    def test_shadowing_import_from_2(self):
        s = """
            from x.a import next

            class A:
                def next(self, a, b):
                    pass
            """
        self.warns_unchanged(s, "Calls to builtin next() possibly shadowed")

    def test_shadowing_import_from_3(self):
        s = """
            from x import a, next, b

            class A:
                def next(self, a, b):
                    pass
            """
        self.warns_unchanged(s, "Calls to builtin next() possibly shadowed")

    def test_shadowing_import_from_4(self):
        s = """
            from x.a import a, next, b

            class A:
                def next(self, a, b):
                    pass
            """
        self.warns_unchanged(s, "Calls to builtin next() possibly shadowed")

    def test_shadowing_funcdef_1(self):
        s = """
            def next(a):
                pass

            class A:
                def next(self, a, b):
                    pass
            """
        self.warns_unchanged(s, "Calls to builtin next() possibly shadowed")

    def test_shadowing_funcdef_2(self):
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
        self.warns(b, a, "Calls to builtin next() possibly shadowed")

    def test_shadowing_global_1(self):
        s = """
            def f():
                global next
                next = 5
            """
        self.warns_unchanged(s, "Calls to builtin next() possibly shadowed")

    def test_shadowing_global_2(self):
        s = """
            def f():
                global a, next, b
                next = 5
            """
        self.warns_unchanged(s, "Calls to builtin next() possibly shadowed")

    def test_shadowing_for_simple(self):
        s = """
            for next in it():
                pass

            b = 5
            c = 6
            """
        self.warns_unchanged(s, "Calls to builtin next() possibly shadowed")

    def test_shadowing_for_tuple_1(self):
        s = """
            for next, b in it():
                pass

            b = 5
            c = 6
            """
        self.warns_unchanged(s, "Calls to builtin next() possibly shadowed")

    def test_shadowing_for_tuple_2(self):
        s = """
            for a, (next, c), b in it():
                pass

            b = 5
            c = 6
            """
        self.warns_unchanged(s, "Calls to builtin next() possibly shadowed")

    def test_noncall_access_1(self):
        b = """gnext = g.next"""
        a = """gnext = g.__next__"""
        self.check(b, a)

    def test_noncall_access_2(self):
        b = """f(g.next + 5)"""
        a = """f(g.__next__ + 5)"""
        self.check(b, a)

    def test_noncall_access_3(self):
        b = """f(g().next + 5)"""
        a = """f(g().__next__ + 5)"""
        self.check(b, a)
