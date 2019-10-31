import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(two_to_three_test_case):
    return two_to_three_test_case("numliterals")


def test_octal_1(fixer):
    b = """0755"""
    a = """0o755"""
    fixer.check(b, a)


def test_long_int_1(fixer):
    b = """a = 12L"""
    a = """a = 12"""
    fixer.check(b, a)


def test_long_int_2(fixer):
    b = """a = 12l"""
    a = """a = 12"""
    fixer.check(b, a)


def test_long_hex(fixer):
    b = """b = 0x12l"""
    a = """b = 0x12"""
    fixer.check(b, a)


def test_comments_and_spacing(fixer):
    b = """b =   0x12L"""
    a = """b =   0x12"""
    fixer.check(b, a)

    b = """b = 0755 # spam"""
    a = """b = 0o755 # spam"""
    fixer.check(b, a)


def test_unchanged_int(fixer):
    s = """5"""
    fixer.unchanged(s)


def test_unchanged_float(fixer):
    s = """5.0"""
    fixer.unchanged(s)


def test_unchanged_octal(fixer):
    s = """0o755"""
    fixer.unchanged(s)


def test_unchanged_hex(fixer):
    s = """0xABC"""
    fixer.unchanged(s)


def test_unchanged_exp(fixer):
    s = """5.0e10"""
    fixer.unchanged(s)


def test_unchanged_complex_int(fixer):
    s = """5 + 4j"""
    fixer.unchanged(s)


def test_unchanged_complex_float(fixer):
    s = """5.4 + 4.9j"""
    fixer.unchanged(s)


def test_unchanged_complex_bare(fixer):
    s = """4j"""
    fixer.unchanged(s)
    s = """4.4j"""
    fixer.unchanged(s)
