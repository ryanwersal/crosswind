import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(three_to_two_test_case):
    return three_to_two_test_case("unittest")


def test_imported(fixer):
    b = "import unittest"
    a = "import unittest2"
    fixer.check(b, a)


def test_used(fixer):
    b = "unittest.AssertStuff(True)"
    a = "unittest2.AssertStuff(True)"
    fixer.check(b, a)


def test_from_import(fixer):
    b = "from unittest import *"
    a = "from unittest2 import *"
    fixer.check(b, a)


def test_imported_from(fixer):
    s = "from whatever import unittest"
    fixer.unchanged(s)


def test_not_base(fixer):
    s = "not_unittest.unittest.stuff()"
    fixer.unchanged(s)
