import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(three_to_two_test_case):
    return three_to_two_test_case("super")


def test_noargs(fixer):

    b = "def m(self):\n    super()"
    a = "def m(self):\n    super(self.__class__, self)"
    fixer.check(b, a)


def test_other_params(fixer):

    b = "def m(a, self=None):\n    super()"
    a = "def m(a, self=None):\n    super(a.__class__, a)"
    fixer.check(b, a)


def test_no_with_stars(fixer):

    s = "def m(*args, **kwargs):\n    super()"
    fixer.unchanged(s, ignore_warnings=True)


def test_no_with_noargs(fixer):

    s = "def m():\n    super()"
    fixer.unchanged(s, ignore_warnings=True)


def test_class_noargs(fixer):

    b = "class c:\n    def m(self):\n        super()"
    a = "class c:\n    def m(self):\n        super(c, self)"
    fixer.check(b, a)


def test_class_other_params(fixer):

    b = "class c:\n    def m(a, self=None):\n        super()"
    a = "class c:\n    def m(a, self=None):\n        super(c, a)"
    fixer.check(b, a)


def test_class_no_with_stars(fixer):

    s = "class c:\n    def m(*args, **kwargs):\n        super()"
    fixer.unchanged(s, ignore_warnings=True)


def test_class_no_with_noargs(fixer):

    s = "class c:\n    def m():\n        super()"
    fixer.unchanged(s, ignore_warnings=True)
