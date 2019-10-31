import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(two_to_three_test_case):
    return two_to_three_test_case("renames")


modules = {"sys": ("maxint", "maxsize")}


def test_import_from(fixer):
    for mod, (old, new) in list(modules.items()):
        b = "from %s import %s" % (mod, old)
        a = "from %s import %s" % (mod, new)
        fixer.check(b, a)

        s = "from foo import %s" % old
        fixer.unchanged(s)


def test_import_from_as(fixer):
    for mod, (old, new) in list(modules.items()):
        b = "from %s import %s as foo_bar" % (mod, old)
        a = "from %s import %s as foo_bar" % (mod, new)
        fixer.check(b, a)


def test_import_module_usage(fixer):
    for mod, (old, new) in list(modules.items()):
        b = """
            import %s
            foo(%s, %s.%s)
            """ % (
            mod,
            mod,
            mod,
            old,
        )
        a = """
            import %s
            foo(%s, %s.%s)
            """ % (
            mod,
            mod,
            mod,
            new,
        )
        fixer.check(b, a)


def XXX_test_from_import_usage(fixer):
    # not implemented yet
    for mod, (old, new) in list(modules.items()):
        b = """
            from %s import %s
            foo(%s, %s)
            """ % (
            mod,
            old,
            mod,
            old,
        )
        a = """
            from %s import %s
            foo(%s, %s)
            """ % (
            mod,
            new,
            mod,
            new,
        )
        fixer.check(b, a)
