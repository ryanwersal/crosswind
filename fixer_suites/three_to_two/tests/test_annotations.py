import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(three_to_two_test_case):
    return three_to_two_test_case("annotations")


def test_return_annotations_alone(fixer):
    b = "def foo() -> 'bar': pass"
    a = "def foo(): pass"
    fixer.check(b, a, ignore_warnings=True)

    b = """
    def foo() -> "bar":
        print "baz"
        print "what's next, again?"
    """
    a = """
    def foo():
        print "baz"
        print "what's next, again?"
    """
    fixer.check(b, a, ignore_warnings=True)


def test_single_param_annotations(fixer):
    b = "def foo(bar:'baz'): pass"
    a = "def foo(bar): pass"
    fixer.check(b, a, ignore_warnings=True)

    b = """
    def foo(bar:"baz"="spam"):
        print "what's next, again?"
        print "whatever."
    """
    a = """
    def foo(bar="spam"):
        print "what's next, again?"
        print "whatever."
    """
    fixer.check(b, a, ignore_warnings=True)


def test_multiple_param_annotations(fixer):
    b = "def foo(bar:'spam'=False, baz:'eggs'=True, ham:False='spaghetti'): pass"
    a = "def foo(bar=False, baz=True, ham='spaghetti'): pass"
    fixer.check(b, a, ignore_warnings=True)

    b = """
    def foo(bar:"spam"=False, baz:"eggs"=True, ham:False="spam"):
        print "this is filler, just doing a suite"
        print "suites require multiple lines."
    """
    a = """
    def foo(bar=False, baz=True, ham="spam"):
        print "this is filler, just doing a suite"
        print "suites require multiple lines."
    """
    fixer.check(b, a, ignore_warnings=True)


def test_mixed_annotations(fixer):
    b = "def foo(bar=False, baz:'eggs'=True, ham:False='spaghetti') -> 'zombies': pass"
    a = "def foo(bar=False, baz=True, ham='spaghetti'): pass"
    fixer.check(b, a, ignore_warnings=True)

    b = """
    def foo(bar:"spam"=False, baz=True, ham:False="spam") -> 'air':
        print "this is filler, just doing a suite"
        print "suites require multiple lines."
    """
    a = """
    def foo(bar=False, baz=True, ham="spam"):
        print "this is filler, just doing a suite"
        print "suites require multiple lines."
    """
    fixer.check(b, a, ignore_warnings=True)

    b = "def foo(bar) -> 'brains': pass"
    a = "def foo(bar): pass"
    fixer.check(b, a, ignore_warnings=True)


def test_unchanged(fixer):
    s = "def foo(): pass"
    fixer.unchanged(s)

    s = """
    def foo():
        pass
        pass
    """
    fixer.unchanged(s)

    s = """
    def foo(bar=baz):
        pass
        pass
    """
    fixer.unchanged(s)
