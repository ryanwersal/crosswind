import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(two_to_three_test_case):
    return two_to_three_test_case("execfile")


def test_conversion(fixer):
    b = """execfile("fn")"""
    a = """exec(compile(open("fn", "rb").read(), "fn", 'exec'))"""
    fixer.check(b, a)

    b = """execfile("fn", glob)"""
    a = """exec(compile(open("fn", "rb").read(), "fn", 'exec'), glob)"""
    fixer.check(b, a)

    b = """execfile("fn", glob, loc)"""
    a = """exec(compile(open("fn", "rb").read(), "fn", 'exec'), glob, loc)"""
    fixer.check(b, a)

    b = """execfile("fn", globals=glob)"""
    a = """exec(compile(open("fn", "rb").read(), "fn", 'exec'), globals=glob)"""
    fixer.check(b, a)

    b = """execfile("fn", locals=loc)"""
    a = """exec(compile(open("fn", "rb").read(), "fn", 'exec'), locals=loc)"""
    fixer.check(b, a)

    b = """execfile("fn", globals=glob, locals=loc)"""
    a = """exec(compile(open("fn", "rb").read(), "fn", 'exec'), globals=glob, locals=loc)"""
    fixer.check(b, a)


def test_spacing(fixer):
    b = """execfile( "fn" )"""
    a = """exec(compile(open( "fn", "rb" ).read(), "fn", 'exec'))"""
    fixer.check(b, a)

    b = """execfile("fn",  globals = glob)"""
    a = """exec(compile(open("fn", "rb").read(), "fn", 'exec'),  globals = glob)"""
    fixer.check(b, a)
