import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(two_to_three_test_case):
    return two_to_three_test_case("exitfunc")


def test_simple(fixer):
    b = """
        import sys
        sys.exitfunc = my_atexit
        """
    a = """
        import sys
        import atexit
        atexit.register(my_atexit)
        """
    fixer.check(b, a)


def test_names_import(fixer):
    b = """
        import sys, crumbs
        sys.exitfunc = my_func
        """
    a = """
        import sys, crumbs, atexit
        atexit.register(my_func)
        """
    fixer.check(b, a)


def test_complex_expression(fixer):
    b = """
        import sys
        sys.exitfunc = do(d)/a()+complex(f=23, g=23)*expression
        """
    a = """
        import sys
        import atexit
        atexit.register(do(d)/a()+complex(f=23, g=23)*expression)
        """
    fixer.check(b, a)


def test_comments(fixer):
    b = """
        import sys # Foo
        sys.exitfunc = f # Blah
        """
    a = """
        import sys
        import atexit # Foo
        atexit.register(f) # Blah
        """
    fixer.check(b, a)

    b = """
        import apples, sys, crumbs, larry # Pleasant comments
        sys.exitfunc = func
        """
    a = """
        import apples, sys, crumbs, larry, atexit # Pleasant comments
        atexit.register(func)
        """
    fixer.check(b, a)


def test_in_a_function(fixer):
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
    fixer.check(b, a)


def test_no_sys_import(fixer):
    b = """sys.exitfunc = f"""
    a = """atexit.register(f)"""
    msg = "Can't find sys import; Please add an atexit import at the top of your file."
    fixer.warns(b, a, msg)


def test_unchanged(fixer):
    s = """f(sys.exitfunc)"""
    fixer.unchanged(s)
