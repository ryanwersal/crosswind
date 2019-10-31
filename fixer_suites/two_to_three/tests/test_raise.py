import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(two_to_three_test_case):
    return two_to_three_test_case("raise")


def test_basic(fixer):
    b = """raise Exception, 5"""
    a = """raise Exception(5)"""
    fixer.check(b, a)


def test_prefix_preservation(fixer):
    b = """raise Exception,5"""
    a = """raise Exception(5)"""
    fixer.check(b, a)

    b = """raise   Exception,    5"""
    a = """raise   Exception(5)"""
    fixer.check(b, a)


def test_with_comments(fixer):
    b = """raise Exception, 5 # foo"""
    a = """raise Exception(5) # foo"""
    fixer.check(b, a)

    b = """raise E, (5, 6) % (a, b) # foo"""
    a = """raise E((5, 6) % (a, b)) # foo"""
    fixer.check(b, a)

    b = """def foo():
                raise Exception, 5, 6 # foo"""
    a = """def foo():
                raise Exception(5).with_traceback(6) # foo"""
    fixer.check(b, a)


def test_None_value(fixer):
    b = """raise Exception(5), None, tb"""
    a = """raise Exception(5).with_traceback(tb)"""
    fixer.check(b, a)


def test_tuple_value(fixer):
    b = """raise Exception, (5, 6, 7)"""
    a = """raise Exception(5, 6, 7)"""
    fixer.check(b, a)


def test_tuple_detection(fixer):
    b = """raise E, (5, 6) % (a, b)"""
    a = """raise E((5, 6) % (a, b))"""
    fixer.check(b, a)


def test_tuple_exc_1(fixer):
    b = """raise (((E1, E2), E3), E4), V"""
    a = """raise E1(V)"""
    fixer.check(b, a)


def test_tuple_exc_2(fixer):
    b = """raise (E1, (E2, E3), E4), V"""
    a = """raise E1(V)"""
    fixer.check(b, a)


# These should produce a warning


def test_string_exc(fixer):
    s = """raise 'foo'"""
    fixer.warns_unchanged(s, "Python 3 does not support string exceptions")


def test_string_exc_val(fixer):
    s = """raise "foo", 5"""
    fixer.warns_unchanged(s, "Python 3 does not support string exceptions")


def test_string_exc_val_tb(fixer):
    s = """raise "foo", 5, 6"""
    fixer.warns_unchanged(s, "Python 3 does not support string exceptions")


# These should result in traceback-assignment


def test_tb_1(fixer):
    b = """def foo():
                raise Exception, 5, 6"""
    a = """def foo():
                raise Exception(5).with_traceback(6)"""
    fixer.check(b, a)


def test_tb_2(fixer):
    b = """def foo():
                a = 5
                raise Exception, 5, 6
                b = 6"""
    a = """def foo():
                a = 5
                raise Exception(5).with_traceback(6)
                b = 6"""
    fixer.check(b, a)


def test_tb_3(fixer):
    b = """def foo():
                raise Exception,5,6"""
    a = """def foo():
                raise Exception(5).with_traceback(6)"""
    fixer.check(b, a)


def test_tb_4(fixer):
    b = """def foo():
                a = 5
                raise Exception,5,6
                b = 6"""
    a = """def foo():
                a = 5
                raise Exception(5).with_traceback(6)
                b = 6"""
    fixer.check(b, a)


def test_tb_5(fixer):
    b = """def foo():
                raise Exception, (5, 6, 7), 6"""
    a = """def foo():
                raise Exception(5, 6, 7).with_traceback(6)"""
    fixer.check(b, a)


def test_tb_6(fixer):
    b = """def foo():
                a = 5
                raise Exception, (5, 6, 7), 6
                b = 6"""
    a = """def foo():
                a = 5
                raise Exception(5, 6, 7).with_traceback(6)
                b = 6"""
    fixer.check(b, a)
