import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(two_to_three_test_case):
    from ..fixes.fix_imports2 import MAPPING as modules

    test_case = two_to_three_test_case("imports2")
    test_case.modules = modules
    return test_case


def test_import_module(fixer):
    for old, new in fixer.modules.items():
        b = "import %s" % old
        a = "import %s" % new
        fixer.check(b, a)

        b = "import foo, %s, bar" % old
        a = "import foo, %s, bar" % new
        fixer.check(b, a)


def test_import_from(fixer):
    for old, new in fixer.modules.items():
        b = "from %s import foo" % old
        a = "from %s import foo" % new
        fixer.check(b, a)

        b = "from %s import foo, bar" % old
        a = "from %s import foo, bar" % new
        fixer.check(b, a)

        b = "from %s import (yes, no)" % old
        a = "from %s import (yes, no)" % new
        fixer.check(b, a)


def test_import_module_as(fixer):
    for old, new in fixer.modules.items():
        b = "import %s as foo_bar" % old
        a = "import %s as foo_bar" % new
        fixer.check(b, a)

        b = "import %s as foo_bar" % old
        a = "import %s as foo_bar" % new
        fixer.check(b, a)


def test_import_from_as(fixer):
    for old, new in fixer.modules.items():
        b = "from %s import foo as bar" % old
        a = "from %s import foo as bar" % new
        fixer.check(b, a)


def test_star(fixer):
    for old, new in fixer.modules.items():
        b = "from %s import *" % old
        a = "from %s import *" % new
        fixer.check(b, a)


def test_import_module_usage(fixer):
    for old, new in fixer.modules.items():
        b = """
            import %s
            foo(%s.bar)
            """ % (
            old,
            old,
        )
        a = """
            import %s
            foo(%s.bar)
            """ % (
            new,
            new,
        )
        fixer.check(b, a)

        b = """
            from %s import x
            %s = 23
            """ % (
            old,
            old,
        )
        a = """
            from %s import x
            %s = 23
            """ % (
            new,
            old,
        )
        fixer.check(b, a)

        s = """
            def f():
                %s.method()
            """ % (
            old,
        )
        fixer.unchanged(s)

        # test nested usage
        b = """
            import %s
            %s.bar(%s.foo)
            """ % (
            old,
            old,
            old,
        )
        a = """
            import %s
            %s.bar(%s.foo)
            """ % (
            new,
            new,
            new,
        )
        fixer.check(b, a)

        b = """
            import %s
            x.%s
            """ % (
            old,
            old,
        )
        a = """
            import %s
            x.%s
            """ % (
            new,
            old,
        )
        fixer.check(b, a)
