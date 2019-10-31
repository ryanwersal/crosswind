import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(three_to_two_test_case):
    return three_to_two_test_case("absimport")


def test_import(fixer):
    a = "import abc"
    b = "from __future__ import absolute_import\nimport abc"

    fixer.check(a, b)


def test_no_imports(fixer):
    a = "2+2"

    fixer.unchanged(a)
