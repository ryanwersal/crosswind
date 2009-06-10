from lib3to2.tests.test_all_fixers import lib3to2FixerTestCase

class Test_numliterals(lib3to2FixerTestCase):
    fixer = "numliterals"

    def test_octal_1(self):
        b = """0o755"""
        a = """0755"""
        self.check(b, a)

    def test_long_int(self):
        b = """a = 12"""
        a = """a = 12L"""
        self.check(b, a)

    def test_long_hex(self):
        b = """b = 0x12"""
        a = """b = __builtins__.long("12", 16)"""
        self.check(b, a)

    def test_comments_and_spacing(self):
        b = """b =   0x12"""
        a = """b =   __builtins__.long("12", 16)"""
        self.check(b, a)

        b = """b = 0o755 # spam"""
        a = """b = 0755 # spam"""
        self.check(b, a)

    def test_unchanged_int(self):
        s = """5"""
        self.unchanged(s)

    def test_unchanged_float(self):
        s = """5.0"""
        self.unchanged(s)

    def test_more_octal(self):
        b = """0o777"""
        a = """0777"""
        self.check(b, a)

    def test_hex(self):
        b = """0xABC"""
        a = """__builtins__.long("ABC", 16)"""
        self.check(b, a)

    def test_bin(self):
        b = """0b10010110"""
        a = """__builtins__.long("10010110", 2)"""
        self.check(b, a)
        
    def test_unchanged_exp(self):
        s = """5.0e10"""
        self.unchanged(s)

    def test_unchanged_complex_int(self):
        s = """5 + 4j"""
        self.unchanged(s)

    def test_unchanged_complex_float(self):
        s = """5.4 + 4.9j"""
        self.unchanged(s)

    def test_unchanged_complex_bare(self):
        s = """4j"""
        self.unchanged(s)
        s = """4.4j"""
        self.unchanged(s)
