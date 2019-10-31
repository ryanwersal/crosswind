import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(two_to_three_test_case):
    return two_to_three_test_case("reduce")


def test_simple_call(fixer):
    b = "reduce(a, b, c)"
    a = "from functools import reduce\nreduce(a, b, c)"
    fixer.check(b, a)


def test_bug_7253(fixer):
    # fix_tuple_params was being bad and orphaning nodes in the tree.
    b = "def x(arg): reduce(sum, [])"
    a = "from functools import reduce\ndef x(arg): reduce(sum, [])"
    fixer.check(b, a)


def test_call_with_lambda(fixer):
    b = "reduce(lambda x, y: x + y, seq)"
    a = "from functools import reduce\nreduce(lambda x, y: x + y, seq)"
    fixer.check(b, a)


def test_unchanged(fixer):
    s = "reduce(a)"
    fixer.unchanged(s)

    s = "reduce(a, b=42)"
    fixer.unchanged(s)

    s = "reduce(a, b, c, d)"
    fixer.unchanged(s)

    s = "reduce(**c)"
    fixer.unchanged(s)

    s = "reduce()"
    fixer.unchanged(s)
