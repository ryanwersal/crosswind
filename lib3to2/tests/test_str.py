from lib3to2.tests.test_all_fixers import lib3to2FixerTestCase

class Test_str(lib3to2FixerTestCase):
    fixer = "str"

    def test_unicode_call(self):
        b = """str(x, y, z)"""
        a = """unicode(x, y, z)"""
        self.check(b, a)

    def test_unicode_literal_1(self):
        b = '''"x"'''
        a = '''u"x"'''
        self.check(b, a)

    def test_unicode_literal_2(self):
        b = """r'x'"""
        a = """ur'x'"""
        self.check(b, a)

    def test_unicode_literal_3(self):
        b = """R'''x'''"""
        a = """uR'''x'''"""
        self.check(b, a)

