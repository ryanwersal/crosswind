import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(three_to_two_test_case):
    return three_to_two_test_case("raise")


def test_unchanged(fixer):
    """
    Due to raise E(V) being valid in 2.5, this fixer fortunately doesn't
    need to touch code that constructs exception objects without explicit
    tracebacks.
    """

    s = """raise E(V)"""
    fixer.unchanged(s)

    s = """raise E("What?")"""
    fixer.unchanged(s)

    s = """raise"""
    fixer.unchanged(s)


def test_what_doesnt_work(fixer):
    """
    These tests should fail, but don't.  TODO: Uncomment successfully.
    One potential way of making these work is a separate fix_exceptions
    with a lower run order than fix_raise, to communicate to fix_raise how
    to sort out that third argument.

    These items are currently outside the scope of crosswind.
    """

    b = """
    E = BaseException(V).with_traceback(T)
    raise E
    """

    # a = """
    # E = BaseException(V)
    # raise E, V, T
    # """

    # self.check(b, a)
    fixer.unchanged(b)

    b = """
    E = BaseException(V)
    E.__traceback__ = S
    E.__traceback__ = T
    raise E
    """

    # a = """
    # E = BaseException(V)
    # raise E, V, T

    # fixer.check(b, a)
    fixer.unchanged(b)


def test_traceback(fixer):
    """
    This stuff currently works, and is the opposite counterpart to the
    2to3 version of fix_raise.
    """
    b = """raise E(V).with_traceback(T)"""
    a = """raise E, V, T"""
    fixer.check(b, a)

    b = """raise E().with_traceback(T)"""
    a = """raise E, None, T"""
    fixer.check(b, a)

    b = """raise E("Sorry, you cannot do that.").with_traceback(T)"""
    a = """raise E, "Sorry, you cannot do that.", T"""
    fixer.check(b, a)


def test_chain(fixer):
    b = "raise E(V).with_traceback(t) from exc"
    a = "raise E, V, t"
    fixer.check(b, a, ignore_warnings=True)

    b = "raise E(V) from exc"
    a = "raise E(V)"
    fixer.check(b, a, ignore_warnings=True)

    b = "raise eBob.exception from exc"
    a = "raise eBob.exception"
    fixer.check(b, a, ignore_warnings=True)
