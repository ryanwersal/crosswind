import pytest

from crosswind import fixer_util


@pytest.fixture(name="fixer")
def fixer_fixture(two_to_three_test_case):
    return two_to_three_test_case("dict")


def test_prefix_preservation(fixer):
    b = "if   d. keys  (  )  : pass"
    a = "if   list(d. keys  (  ))  : pass"
    fixer.check(b, a)

    b = "if   d. items  (  )  : pass"
    a = "if   list(d. items  (  ))  : pass"
    fixer.check(b, a)

    b = "if   d. iterkeys  ( )  : pass"
    a = "if   iter(d. keys  ( ))  : pass"
    fixer.check(b, a)

    b = "[i for i in    d.  iterkeys(  )  ]"
    a = "[i for i in    d.  keys(  )  ]"
    fixer.check(b, a)

    b = "if   d. viewkeys  ( )  : pass"
    a = "if   d. keys  ( )  : pass"
    fixer.check(b, a)

    b = "[i for i in    d.  viewkeys(  )  ]"
    a = "[i for i in    d.  keys(  )  ]"
    fixer.check(b, a)


def test_trailing_comment(fixer):
    b = "d.keys() # foo"
    a = "list(d.keys()) # foo"
    fixer.check(b, a)

    b = "d.items()  # foo"
    a = "list(d.items())  # foo"
    fixer.check(b, a)

    b = "d.iterkeys()  # foo"
    a = "iter(d.keys())  # foo"
    fixer.check(b, a)

    b = """[i for i in d.iterkeys() # foo
            ]"""
    a = """[i for i in d.keys() # foo
            ]"""
    fixer.check(b, a)

    b = """[i for i in d.iterkeys() # foo
            ]"""
    a = """[i for i in d.keys() # foo
            ]"""
    fixer.check(b, a)

    b = "d.viewitems()  # foo"
    a = "d.items()  # foo"
    fixer.check(b, a)


def test_unchanged(fixer):
    for wrapper in fixer_util.consuming_calls:
        s = "s = %s(d.keys())" % wrapper
        fixer.unchanged(s)

        s = "s = %s(d.values())" % wrapper
        fixer.unchanged(s)

        s = "s = %s(d.items())" % wrapper
        fixer.unchanged(s)


def test_01(fixer):
    b = "d.keys()"
    a = "list(d.keys())"
    fixer.check(b, a)

    b = "a[0].foo().keys()"
    a = "list(a[0].foo().keys())"
    fixer.check(b, a)


def test_02(fixer):
    b = "d.items()"
    a = "list(d.items())"
    fixer.check(b, a)


def test_03(fixer):
    b = "d.values()"
    a = "list(d.values())"
    fixer.check(b, a)


def test_04(fixer):
    b = "d.iterkeys()"
    a = "iter(d.keys())"
    fixer.check(b, a)


def test_05(fixer):
    b = "d.iteritems()"
    a = "iter(d.items())"
    fixer.check(b, a)


def test_06(fixer):
    b = "d.itervalues()"
    a = "iter(d.values())"
    fixer.check(b, a)


def test_07(fixer):
    s = "list(d.keys())"
    fixer.unchanged(s)


def test_08(fixer):
    s = "sorted(d.keys())"
    fixer.unchanged(s)


def test_09(fixer):
    b = "iter(d.keys())"
    a = "iter(list(d.keys()))"
    fixer.check(b, a)


def test_10(fixer):
    b = "foo(d.keys())"
    a = "foo(list(d.keys()))"
    fixer.check(b, a)


def test_11(fixer):
    b = "for i in d.keys(): print i"
    a = "for i in list(d.keys()): print i"
    fixer.check(b, a)


def test_12(fixer):
    b = "for i in d.iterkeys(): print i"
    a = "for i in d.keys(): print i"
    fixer.check(b, a)


def test_13(fixer):
    b = "[i for i in d.keys()]"
    a = "[i for i in list(d.keys())]"
    fixer.check(b, a)


def test_14(fixer):
    b = "[i for i in d.iterkeys()]"
    a = "[i for i in d.keys()]"
    fixer.check(b, a)


def test_15(fixer):
    b = "(i for i in d.keys())"
    a = "(i for i in list(d.keys()))"
    fixer.check(b, a)


def test_16(fixer):
    b = "(i for i in d.iterkeys())"
    a = "(i for i in d.keys())"
    fixer.check(b, a)


def test_17(fixer):
    b = "iter(d.iterkeys())"
    a = "iter(d.keys())"
    fixer.check(b, a)


def test_18(fixer):
    b = "list(d.iterkeys())"
    a = "list(d.keys())"
    fixer.check(b, a)


def test_19(fixer):
    b = "sorted(d.iterkeys())"
    a = "sorted(d.keys())"
    fixer.check(b, a)


def test_20(fixer):
    b = "foo(d.iterkeys())"
    a = "foo(iter(d.keys()))"
    fixer.check(b, a)


def test_21(fixer):
    b = "print h.iterkeys().next()"
    a = "print iter(h.keys()).next()"
    fixer.check(b, a)


def test_22(fixer):
    b = "print h.keys()[0]"
    a = "print list(h.keys())[0]"
    fixer.check(b, a)


def test_23(fixer):
    b = "print list(h.iterkeys().next())"
    a = "print list(iter(h.keys()).next())"
    fixer.check(b, a)


def test_24(fixer):
    b = "for x in h.keys()[0]: print x"
    a = "for x in list(h.keys())[0]: print x"
    fixer.check(b, a)


def test_25(fixer):
    b = "d.viewkeys()"
    a = "d.keys()"
    fixer.check(b, a)


def test_26(fixer):
    b = "d.viewitems()"
    a = "d.items()"
    fixer.check(b, a)


def test_27(fixer):
    b = "d.viewvalues()"
    a = "d.values()"
    fixer.check(b, a)


def test_28(fixer):
    b = "[i for i in d.viewkeys()]"
    a = "[i for i in d.keys()]"
    fixer.check(b, a)


def test_29(fixer):
    b = "(i for i in d.viewkeys())"
    a = "(i for i in d.keys())"
    fixer.check(b, a)


def test_30(fixer):
    b = "iter(d.viewkeys())"
    a = "iter(d.keys())"
    fixer.check(b, a)


def test_31(fixer):
    b = "list(d.viewkeys())"
    a = "list(d.keys())"
    fixer.check(b, a)


def test_32(fixer):
    b = "sorted(d.viewkeys())"
    a = "sorted(d.keys())"
    fixer.check(b, a)
