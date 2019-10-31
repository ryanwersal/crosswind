import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(two_to_three_test_case):
    return two_to_three_test_case("future")


def test_future(fixer):
    b = """from __future__ import braces"""
    a = """"""
    fixer.check(b, a)

    b = """# comment\nfrom __future__ import braces"""
    a = """# comment\n"""
    fixer.check(b, a)

    b = """from __future__ import braces\n# comment"""
    a = """\n# comment"""
    fixer.check(b, a)


def test_run_order(fixer):
    fixer.assert_runs_after("print")
