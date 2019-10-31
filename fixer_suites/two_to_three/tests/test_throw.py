import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(two_to_three_test_case):
    return two_to_three_test_case("throw")


def test_1(fixer):
    b = """g.throw(Exception, 5)"""
    a = """g.throw(Exception(5))"""
    fixer.check(b, a)


def test_2(fixer):
    b = """g.throw(Exception,5)"""
    a = """g.throw(Exception(5))"""
    fixer.check(b, a)


def test_3(fixer):
    b = """g.throw(Exception, (5, 6, 7))"""
    a = """g.throw(Exception(5, 6, 7))"""
    fixer.check(b, a)


def test_4(fixer):
    b = """5 + g.throw(Exception, 5)"""
    a = """5 + g.throw(Exception(5))"""
    fixer.check(b, a)


# These should produce warnings


def test_warn_1(fixer):
    s = """g.throw("foo")"""
    fixer.warns_unchanged(s, "Python 3 does not support string exceptions")


def test_warn_2(fixer):
    s = """g.throw("foo", 5)"""
    fixer.warns_unchanged(s, "Python 3 does not support string exceptions")


def test_warn_3(fixer):
    s = """g.throw("foo", 5, 6)"""
    fixer.warns_unchanged(s, "Python 3 does not support string exceptions")


# These should not be touched


def test_untouched_1(fixer):
    s = """g.throw(Exception)"""
    fixer.unchanged(s)


def test_untouched_2(fixer):
    s = """g.throw(Exception(5, 6))"""
    fixer.unchanged(s)


def test_untouched_3(fixer):
    s = """5 + g.throw(Exception(5, 6))"""
    fixer.unchanged(s)


# These should result in traceback-assignment


def test_tb_1(fixer):
    b = """def foo():
                g.throw(Exception, 5, 6)"""
    a = """def foo():
                g.throw(Exception(5).with_traceback(6))"""
    fixer.check(b, a)


def test_tb_2(fixer):
    b = """def foo():
                a = 5
                g.throw(Exception, 5, 6)
                b = 6"""
    a = """def foo():
                a = 5
                g.throw(Exception(5).with_traceback(6))
                b = 6"""
    fixer.check(b, a)


def test_tb_3(fixer):
    b = """def foo():
                g.throw(Exception,5,6)"""
    a = """def foo():
                g.throw(Exception(5).with_traceback(6))"""
    fixer.check(b, a)


def test_tb_4(fixer):
    b = """def foo():
                a = 5
                g.throw(Exception,5,6)
                b = 6"""
    a = """def foo():
                a = 5
                g.throw(Exception(5).with_traceback(6))
                b = 6"""
    fixer.check(b, a)


def test_tb_5(fixer):
    b = """def foo():
                g.throw(Exception, (5, 6, 7), 6)"""
    a = """def foo():
                g.throw(Exception(5, 6, 7).with_traceback(6))"""
    fixer.check(b, a)


def test_tb_6(fixer):
    b = """def foo():
                a = 5
                g.throw(Exception, (5, 6, 7), 6)
                b = 6"""
    a = """def foo():
                a = 5
                g.throw(Exception(5, 6, 7).with_traceback(6))
                b = 6"""
    fixer.check(b, a)


def test_tb_7(fixer):
    b = """def foo():
                a + g.throw(Exception, 5, 6)"""
    a = """def foo():
                a + g.throw(Exception(5).with_traceback(6))"""
    fixer.check(b, a)


def test_tb_8(fixer):
    b = """def foo():
                a = 5
                a + g.throw(Exception, 5, 6)
                b = 6"""
    a = """def foo():
                a = 5
                a + g.throw(Exception(5).with_traceback(6))
                b = 6"""
    fixer.check(b, a)
