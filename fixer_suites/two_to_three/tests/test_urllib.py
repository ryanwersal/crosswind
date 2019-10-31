from operator import itemgetter

import pytest

from ..fixes.fix_urllib import MAPPING as modules


@pytest.fixture(name="fixer")
def fixer_fixture(two_to_three_test_case):
    return two_to_three_test_case("urllib")


def test_import_module(fixer):
    for old, changes in modules.items():
        b = "import %s" % old
        a = "import %s" % ", ".join(map(itemgetter(0), changes))
        fixer.check(b, a)


def test_import_from(fixer):
    for old, changes in modules.items():
        all_members = []
        for new, members in changes:
            for member in members:
                all_members.append(member)
                b = "from %s import %s" % (old, member)
                a = "from %s import %s" % (new, member)
                fixer.check(b, a)

                s = "from foo import %s" % member
                fixer.unchanged(s)

            b = "from %s import %s" % (old, ", ".join(members))
            a = "from %s import %s" % (new, ", ".join(members))
            fixer.check(b, a)

            s = "from foo import %s" % ", ".join(members)
            fixer.unchanged(s)

        # test the breaking of a module into multiple replacements
        b = "from %s import %s" % (old, ", ".join(all_members))
        a = "\n".join(["from %s import %s" % (new, ", ".join(members)) for (new, members) in changes])
        fixer.check(b, a)


def test_import_module_as(fixer):
    for old in modules:
        s = "import %s as foo" % old
        fixer.warns_unchanged(s, "This module is now multiple modules")


def test_import_from_as(fixer):
    for old, changes in modules.items():
        for new, members in changes:
            for member in members:
                b = "from %s import %s as foo_bar" % (old, member)
                a = "from %s import %s as foo_bar" % (new, member)
                fixer.check(b, a)
                b = "from %s import %s as blah, %s" % (old, member, member)
                a = "from %s import %s as blah, %s" % (new, member, member)
                fixer.check(b, a)


def test_star(fixer):
    for old in modules:
        s = "from %s import *" % old
        fixer.warns_unchanged(s, "Cannot handle star imports")


def test_indented(fixer):
    b = """
def foo():
    from urllib import urlencode, urlopen
"""
    a = """
def foo():
    from urllib.parse import urlencode
    from urllib.request import urlopen
"""
    fixer.check(b, a)

    b = """
def foo():
    other()
    from urllib import urlencode, urlopen
"""
    a = """
def foo():
    other()
    from urllib.parse import urlencode
    from urllib.request import urlopen
"""
    fixer.check(b, a)


def test_import_module_usage(fixer):
    for old, changes in modules.items():
        for new, members in changes:
            for member in members:
                new_import = ", ".join([n for (n, mems) in modules[old]])
                b = """
                    import %s
                    foo(%s.%s)
                    """ % (
                    old,
                    old,
                    member,
                )
                a = """
                    import %s
                    foo(%s.%s)
                    """ % (
                    new_import,
                    new,
                    member,
                )
                fixer.check(b, a)
                b = """
                    import %s
                    %s.%s(%s.%s)
                    """ % (
                    old,
                    old,
                    member,
                    old,
                    member,
                )
                a = """
                    import %s
                    %s.%s(%s.%s)
                    """ % (
                    new_import,
                    new,
                    member,
                    new,
                    member,
                )
                fixer.check(b, a)
