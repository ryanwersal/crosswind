import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(two_to_three_test_case):
    return two_to_three_test_case("future")


def test_removes_future_import(fixer):
    b = """from __future__ import braces"""
    a = """"""
    fixer.check(b, a)


def test_removes_future_import_but_leaves_prior_lines(fixer):
    b = """# comment\nfrom __future__ import braces"""
    a = """# comment\n"""
    fixer.check(b, a)


def test_removes_future_import_but_leaves_trailing_lines(fixer):
    b = """from __future__ import braces\n# comment"""
    a = """\n# comment"""
    fixer.check(b, a)


def test_run_order(fixer):
    fixer.assert_runs_after("print")
