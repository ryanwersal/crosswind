import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(three_to_two_test_case):
    return three_to_two_test_case("bytes")


def test_bytes_call_1(fixer):
    b = """bytes(x)"""
    a = """str(x)"""
    fixer.check(b, a)


def test_bytes_call_2(fixer):
    b = """a = bytes(x) + b"florist" """
    a = """a = str(x) + "florist" """
    fixer.check(b, a)


def test_bytes_call_noargs(fixer):
    b = """bytes()"""
    a = """str()"""
    fixer.check(b, a)


def test_bytes_call_args_1(fixer):
    b = """bytes(x, y, z)"""
    a = """str(x).encode(y, z)"""
    fixer.check(b, a)


def test_bytes_call_args_2(fixer):
    b = """bytes(encoding="utf-8", source="dinosaur", errors="dont-care")"""
    a = """str("dinosaur").encode("utf-8", "dont-care")"""
    fixer.check(b, a)


def test_bytes_literal_1(fixer):
    b = '''b"\x41"'''
    a = '''"\x41"'''
    fixer.check(b, a)


def test_bytes_literal_2(fixer):
    b = """b'x'"""
    a = """'x'"""
    fixer.check(b, a)


def test_bytes_literal_3(fixer):
    b = """BR'''\x13'''"""
    a = """R'''\x13'''"""
    fixer.check(b, a)


def test_bytes_concatenation(fixer):
    b = """b'bytes' + b'bytes'"""
    a = """'bytes' + 'bytes'"""
    fixer.check(b, a)
