import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(three_to_two_test_case):
    return three_to_two_test_case("with")


def test_with_oneline(fixer):
    b = "with a as b: pass"
    a = "from __future__ import with_statement\nwith a as b: pass"
    fixer.check(b, a)


def test_with_suite(fixer):
    b = "with a as b:\n    pass"
    a = "from __future__ import with_statement\nwith a as b:\n    pass"
    fixer.check(b, a)
