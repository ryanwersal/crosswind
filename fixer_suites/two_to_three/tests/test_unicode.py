import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(two_to_three_test_case):
    return two_to_three_test_case("unicode")


def test_whitespace(fixer):
    b = """unicode( x)"""
    a = """str( x)"""
    fixer.check(b, a)

    b = """ unicode(x )"""
    a = """ str(x )"""
    fixer.check(b, a)

    b = """ u'h'"""
    a = """ 'h'"""
    fixer.check(b, a)


def test_unicode_call(fixer):
    b = """unicode(x, y, z)"""
    a = """str(x, y, z)"""
    fixer.check(b, a)


def test_chained_unicode_call(fixer):
    b = """return unicode(x).lower()"""
    a = """return str(x).lower()"""
    fixer.check(b, a)


def test_unichr(fixer):
    b = """unichr(u'h')"""
    a = """chr('h')"""
    fixer.check(b, a)


def test_unicode_literal_1(fixer):
    b = '''u"x"'''
    a = '''"x"'''
    fixer.check(b, a)


def test_unicode_literal_2(fixer):
    b = """ur'x'"""
    a = """r'x'"""
    fixer.check(b, a)


def test_unicode_literal_3(fixer):
    b = """UR'''x''' """
    a = """R'''x''' """
    fixer.check(b, a)


def test_native_literal_escape_u(fixer):
    b = r"""'\\\u20ac\U0001d121\\u20ac'"""
    a = r"""'\\\\u20ac\\U0001d121\\u20ac'"""
    fixer.check(b, a)

    b = r"""r'\\\u20ac\U0001d121\\u20ac'"""
    a = r"""r'\\\u20ac\U0001d121\\u20ac'"""
    fixer.check(b, a)


def test_bytes_literal_escape_u(fixer):
    b = r"""b'\\\u20ac\U0001d121\\u20ac'"""
    a = r"""b'\\\u20ac\U0001d121\\u20ac'"""
    fixer.check(b, a)

    b = r"""br'\\\u20ac\U0001d121\\u20ac'"""
    a = r"""br'\\\u20ac\U0001d121\\u20ac'"""
    fixer.check(b, a)


def test_unicode_literal_escape_u(fixer):
    b = r"""u'\\\u20ac\U0001d121\\u20ac'"""
    a = r"""'\\\u20ac\U0001d121\\u20ac'"""
    fixer.check(b, a)

    b = r"""ur'\\\u20ac\U0001d121\\u20ac'"""
    a = r"""r'\\\u20ac\U0001d121\\u20ac'"""
    fixer.check(b, a)


def test_native_unicode_literal_escape_u(fixer):
    f = "from __future__ import unicode_literals\n"
    b = f + r"""'\\\u20ac\U0001d121\\u20ac'"""
    a = f + r"""'\\\u20ac\U0001d121\\u20ac'"""
    fixer.check(b, a)

    b = f + r"""r'\\\u20ac\U0001d121\\u20ac'"""
    a = f + r"""r'\\\u20ac\U0001d121\\u20ac'"""
    fixer.check(b, a)
