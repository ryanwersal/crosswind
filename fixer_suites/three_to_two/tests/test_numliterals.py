import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(three_to_two_test_case):
    return three_to_two_test_case("numliterals")


def test_octal_1(fixer):
    b = """0o755"""
    a = """0755"""
    fixer.check(b, a)


def test_octal_2(fixer):
    b = """0o777"""
    a = """0777"""
    fixer.check(b, a)


def test_bin_1(fixer):
    b = """0b10010110"""
    a = """__builtins__.long("10010110", 2)"""
    fixer.check(b, a)


def test_bin_2(fixer):
    b = """spam(0b1101011010110)"""
    a = """spam(__builtins__.long("1101011010110", 2))"""
    fixer.check(b, a)


def test_comments_and_spacing_2(fixer):
    b = """b = 0o755 # spam"""
    a = """b = 0755 # spam"""
    fixer.check(b, a)


def test_unchanged_str(fixer):
    s = """'0x1400'"""
    fixer.unchanged(s)

    s = """'0b011000'"""
    fixer.unchanged(s)

    s = """'0o755'"""
    fixer.unchanged(s)


def test_unchanged_other(fixer):
    s = """5.0"""
    fixer.unchanged(s)

    s = """5.0e10"""
    fixer.unchanged(s)

    s = """5.4 + 4.9j"""
    fixer.unchanged(s)

    s = """4j"""
    fixer.unchanged(s)

    s = """4.4j"""
    fixer.unchanged(s)
