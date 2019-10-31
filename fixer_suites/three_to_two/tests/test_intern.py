import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(three_to_two_test_case):
    return three_to_two_test_case("intern")


# XXX: Does not remove unused "import sys" lines.
def test_prefix_preservation(fixer):
    b = """import sys\nx =   sys.intern(  a  )"""
    a = """import sys\nx =   intern(  a  )"""
    fixer.check(b, a)

    b = """import sys\ny = sys.intern("b" # test
            )"""
    a = """import sys\ny = intern("b" # test
            )"""
    fixer.check(b, a)

    b = """import sys\nz = sys.intern(a+b+c.d,   )"""
    a = """import sys\nz = intern(a+b+c.d,   )"""
    fixer.check(b, a)


def test(fixer):
    b = """from sys import intern\nx = intern(a)"""
    a = """\nx = intern(a)"""
    fixer.check(b, a)

    b = """import sys\nz = sys.intern(a+b+c.d,)"""
    a = """import sys\nz = intern(a+b+c.d,)"""
    fixer.check(b, a)

    b = """import sys\nsys.intern("y%s" % 5).replace("y", "")"""
    a = """import sys\nintern("y%s" % 5).replace("y", "")"""
    fixer.check(b, a)


# These should not be refactored


def test_multimports(fixer):
    b = """from sys import intern, path"""
    a = """from sys import path"""
    fixer.check(b, a)

    b = """from sys import path, intern"""
    a = """from sys import path"""
    fixer.check(b, a)

    b = """from sys import argv, intern, path"""
    a = """from sys import argv, path"""
    fixer.check(b, a)


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
