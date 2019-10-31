import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(two_to_three_test_case):
    return two_to_three_test_case("intern")


def test_prefix_preservation(fixer):
    b = """x =   intern(  a  )"""
    a = """import sys\nx =   sys.intern(  a  )"""
    fixer.check(b, a)

    b = """y = intern("b" # test
            )"""
    a = """import sys\ny = sys.intern("b" # test
            )"""
    fixer.check(b, a)

    b = """z = intern(a+b+c.d,   )"""
    a = """import sys\nz = sys.intern(a+b+c.d,   )"""
    fixer.check(b, a)


def test(fixer):
    b = """x = intern(a)"""
    a = """import sys\nx = sys.intern(a)"""
    fixer.check(b, a)

    b = """z = intern(a+b+c.d,)"""
    a = """import sys\nz = sys.intern(a+b+c.d,)"""
    fixer.check(b, a)

    b = """intern("y%s" % 5).replace("y", "")"""
    a = """import sys\nsys.intern("y%s" % 5).replace("y", "")"""
    fixer.check(b, a)


# These should not be refactored


def test_unchanged(fixer):
    s = """intern(a=1)"""
    fixer.unchanged(s)

    s = """intern(f, g)"""
    fixer.unchanged(s)

    s = """intern(*h)"""
    fixer.unchanged(s)

    s = """intern(**i)"""
    fixer.unchanged(s)

    s = """intern()"""
    fixer.unchanged(s)
