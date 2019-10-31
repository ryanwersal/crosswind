import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(two_to_three_test_case):
    return two_to_three_test_case("itertools_imports")


def test_reduced(fixer):
    b = "from itertools import imap, izip, foo"
    a = "from itertools import foo"
    fixer.check(b, a)

    b = "from itertools import bar, imap, izip, foo"
    a = "from itertools import bar, foo"
    fixer.check(b, a)

    b = "from itertools import chain, imap, izip"
    a = "from itertools import chain"
    fixer.check(b, a)


def test_comments(fixer):
    b = "#foo\nfrom itertools import imap, izip"
    a = "#foo\n"
    fixer.check(b, a)


def test_none(fixer):
    b = "from itertools import imap, izip"
    a = ""
    fixer.check(b, a)

    b = "from itertools import izip"
    a = ""
    fixer.check(b, a)


def test_import_as(fixer):
    b = "from itertools import izip, bar as bang, imap"
    a = "from itertools import bar as bang"
    fixer.check(b, a)

    b = "from itertools import izip as _zip, imap, bar"
    a = "from itertools import bar"
    fixer.check(b, a)

    b = "from itertools import imap as _map"
    a = ""
    fixer.check(b, a)

    b = "from itertools import imap as _map, izip as _zip"
    a = ""
    fixer.check(b, a)

    s = "from itertools import bar as bang"
    fixer.unchanged(s)


def test_ifilter_and_zip_longest(fixer):
    for name in "filterfalse", "zip_longest":
        b = "from itertools import i%s" % (name,)
        a = "from itertools import %s" % (name,)
        fixer.check(b, a)

        b = "from itertools import imap, i%s, foo" % (name,)
        a = "from itertools import %s, foo" % (name,)
        fixer.check(b, a)

        b = "from itertools import bar, i%s, foo" % (name,)
        a = "from itertools import bar, %s, foo" % (name,)
        fixer.check(b, a)


def test_import_star(fixer):
    s = "from itertools import *"
    fixer.unchanged(s)


def test_unchanged(fixer):
    s = "from itertools import foo"
    fixer.unchanged(s)
