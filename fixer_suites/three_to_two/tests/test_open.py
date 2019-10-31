import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(three_to_two_test_case):
    return three_to_two_test_case("open")


def test_imports(fixer):
    b = """new_file = open("some_filename", newline="\\r")"""
    a = """from io import open\nnew_file = open("some_filename", newline="\\r")"""
    fixer.check(b, a)


def test_doesnt_import(fixer):
    s = """new_file = nothing.open("some_filename")"""
    fixer.unchanged(s)
