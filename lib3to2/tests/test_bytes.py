from lib3to2.tests.test_all_fixers import lib3to2FixerTestCase

class Test_bytes(lib3to2FixerTestCase):
    fixer = "bytes"

    def test_bytes_call(self):
        b = """bytes(x, y, z)"""
        a = """str(x, y, z)"""
        self.check(b, a)

    def test_bytes_literal_1(self):
        b = '''b"\x41"'''
        a = '''"\x41"'''
        self.check(b, a)

    def test_bytes_literal_2(self):
        b = """b'x'"""
        a = """'x'"""
        self.check(b, a)

    def test_bytes_literal_3(self):
        b = """BR'''\x13'''"""
        a = """R'''\x13'''"""
        self.check(b, a)

    def test_bytes_concatenation(self):
        b = """b'bytes' + b'bytes'"""
        a = """'bytes' + 'bytes'"""
        self.check(b, a)
