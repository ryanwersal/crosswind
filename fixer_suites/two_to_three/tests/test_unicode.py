from crosswind.tests.support import FixerTestCase


class Test_unicode(FixerTestCase):
    fixer = "unicode"

    def test_whitespace(self):
        b = """unicode( x)"""
        a = """str( x)"""
        self.check(b, a)

        b = """ unicode(x )"""
        a = """ str(x )"""
        self.check(b, a)

        b = """ u'h'"""
        a = """ 'h'"""
        self.check(b, a)

    def test_unicode_call(self):
        b = """unicode(x, y, z)"""
        a = """str(x, y, z)"""
        self.check(b, a)

    def test_chained_unicode_call(self):
        b = """return unicode(x).lower()"""
        a = """return str(x).lower()"""
        self.check(b, a)

    def test_unichr(self):
        b = """unichr(u'h')"""
        a = """chr('h')"""
        self.check(b, a)

    def test_unicode_literal_1(self):
        b = '''u"x"'''
        a = '''"x"'''
        self.check(b, a)

    def test_unicode_literal_2(self):
        b = """ur'x'"""
        a = """r'x'"""
        self.check(b, a)

    def test_unicode_literal_3(self):
        b = """UR'''x''' """
        a = """R'''x''' """
        self.check(b, a)

    def test_native_literal_escape_u(self):
        b = r"""'\\\u20ac\U0001d121\\u20ac'"""
        a = r"""'\\\\u20ac\\U0001d121\\u20ac'"""
        self.check(b, a)

        b = r"""r'\\\u20ac\U0001d121\\u20ac'"""
        a = r"""r'\\\u20ac\U0001d121\\u20ac'"""
        self.check(b, a)

    def test_bytes_literal_escape_u(self):
        b = r"""b'\\\u20ac\U0001d121\\u20ac'"""
        a = r"""b'\\\u20ac\U0001d121\\u20ac'"""
        self.check(b, a)

        b = r"""br'\\\u20ac\U0001d121\\u20ac'"""
        a = r"""br'\\\u20ac\U0001d121\\u20ac'"""
        self.check(b, a)

    def test_unicode_literal_escape_u(self):
        b = r"""u'\\\u20ac\U0001d121\\u20ac'"""
        a = r"""'\\\u20ac\U0001d121\\u20ac'"""
        self.check(b, a)

        b = r"""ur'\\\u20ac\U0001d121\\u20ac'"""
        a = r"""r'\\\u20ac\U0001d121\\u20ac'"""
        self.check(b, a)

    def test_native_unicode_literal_escape_u(self):
        f = "from __future__ import unicode_literals\n"
        b = f + r"""'\\\u20ac\U0001d121\\u20ac'"""
        a = f + r"""'\\\u20ac\U0001d121\\u20ac'"""
        self.check(b, a)

        b = f + r"""r'\\\u20ac\U0001d121\\u20ac'"""
        a = f + r"""r'\\\u20ac\U0001d121\\u20ac'"""
        self.check(b, a)
