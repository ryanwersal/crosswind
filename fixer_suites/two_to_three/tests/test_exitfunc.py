from crosswind.tests.support import FixerTestCase


class Test_exitfunc(FixerTestCase):

    fixer = "exitfunc"

    def test_simple(self):
        b = """
            import sys
            sys.exitfunc = my_atexit
            """
        a = """
            import sys
            import atexit
            atexit.register(my_atexit)
            """
        self.check(b, a)

    def test_names_import(self):
        b = """
            import sys, crumbs
            sys.exitfunc = my_func
            """
        a = """
            import sys, crumbs, atexit
            atexit.register(my_func)
            """
        self.check(b, a)

    def test_complex_expression(self):
        b = """
            import sys
            sys.exitfunc = do(d)/a()+complex(f=23, g=23)*expression
            """
        a = """
            import sys
            import atexit
            atexit.register(do(d)/a()+complex(f=23, g=23)*expression)
            """
        self.check(b, a)

    def test_comments(self):
        b = """
            import sys # Foo
            sys.exitfunc = f # Blah
            """
        a = """
            import sys
            import atexit # Foo
            atexit.register(f) # Blah
            """
        self.check(b, a)

        b = """
            import apples, sys, crumbs, larry # Pleasant comments
            sys.exitfunc = func
            """
        a = """
            import apples, sys, crumbs, larry, atexit # Pleasant comments
            atexit.register(func)
            """
        self.check(b, a)

    def test_in_a_function(self):
        b = """
            import sys
            def f():
                sys.exitfunc = func
            """
        a = """
            import sys
            import atexit
            def f():
                atexit.register(func)
             """
        self.check(b, a)

    def test_no_sys_import(self):
        b = """sys.exitfunc = f"""
        a = """atexit.register(f)"""
        msg = "Can't find sys import; Please add an atexit import at the top of your file."
        self.warns(b, a, msg)

    def test_unchanged(self):
        s = """f(sys.exitfunc)"""
        self.unchanged(s)
