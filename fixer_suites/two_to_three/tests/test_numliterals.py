from crosswind.tests.support import FixerTestCase


class Test_numliterals(FixerTestCase):
    fixer = "numliterals"

    def test_octal_1(self):
        b = """0755"""
        a = """0o755"""
        self.check(b, a)

    def test_long_int_1(self):
        b = """a = 12L"""
        a = """a = 12"""
        self.check(b, a)

    def test_long_int_2(self):
        b = """a = 12l"""
        a = """a = 12"""
        self.check(b, a)

    def test_long_hex(self):
        b = """b = 0x12l"""
        a = """b = 0x12"""
        self.check(b, a)

    def test_comments_and_spacing(self):
        b = """b =   0x12L"""
        a = """b =   0x12"""
        self.check(b, a)

        b = """b = 0755 # spam"""
        a = """b = 0o755 # spam"""
        self.check(b, a)

    def test_unchanged_int(self):
        s = """5"""
        self.unchanged(s)

    def test_unchanged_float(self):
        s = """5.0"""
        self.unchanged(s)

    def test_unchanged_octal(self):
        s = """0o755"""
        self.unchanged(s)

    def test_unchanged_hex(self):
        s = """0xABC"""
        self.unchanged(s)

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
