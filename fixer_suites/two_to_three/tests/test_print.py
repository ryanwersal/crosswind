import pytest

from crosswind import pygram


@pytest.fixture(name="fixer")
def fixer_fixture(two_to_three_test_case):
    return two_to_three_test_case("print")


@pytest.fixture(name="no_print_fixer")
def no_print_fixture(two_to_three_test_case):
    test_case = two_to_three_test_case("print")
    test_case.refactor.driver.grammar = pygram.python_grammar_no_print_statement
    return test_case


def test_prefix_preservation(fixer):
    b = """print 1,   1+1,   1+1+1"""
    a = """print(1,   1+1,   1+1+1)"""
    fixer.check(b, a)


def test_idempotency(fixer):
    s = """print()"""
    fixer.unchanged(s)

    s = """print('')"""
    fixer.unchanged(s)


def test_idempotency_print_as_function(no_print_fixer):
    s = """print(1, 1+1, 1+1+1)"""
    no_print_fixer.unchanged(s)

    s = """print()"""
    no_print_fixer.unchanged(s)

    s = """print('')"""
    no_print_fixer.unchanged(s)


def test_1(fixer):
    b = """print 1, 1+1, 1+1+1"""
    a = """print(1, 1+1, 1+1+1)"""
    fixer.check(b, a)


def test_2(fixer):
    b = """print 1, 2"""
    a = """print(1, 2)"""
    fixer.check(b, a)


def test_3(fixer):
    b = """print"""
    a = """print()"""
    fixer.check(b, a)


def test_4(fixer):
    # from bug 3000
    b = """print whatever; print"""
    a = """print(whatever); print()"""
    fixer.check(b, a)


def test_5(fixer):
    b = """print; print whatever;"""
    a = """print(); print(whatever);"""
    fixer.check(b, a)


def test_tuple(fixer):
    b = """print (a, b, c)"""
    a = """print((a, b, c))"""
    fixer.check(b, a)


# trailing commas


def test_trailing_comma_1(fixer):
    b = """print 1, 2, 3,"""
    a = """print(1, 2, 3, end=' ')"""
    fixer.check(b, a)


def test_trailing_comma_2(fixer):
    b = """print 1, 2,"""
    a = """print(1, 2, end=' ')"""
    fixer.check(b, a)


def test_trailing_comma_3(fixer):
    b = """print 1,"""
    a = """print(1, end=' ')"""
    fixer.check(b, a)


# >> stuff


def test_vargs_without_trailing_comma(fixer):
    b = """print >>sys.stderr, 1, 2, 3"""
    a = """print(1, 2, 3, file=sys.stderr)"""
    fixer.check(b, a)


def test_with_trailing_comma(fixer):
    b = """print >>sys.stderr, 1, 2,"""
    a = """print(1, 2, end=' ', file=sys.stderr)"""
    fixer.check(b, a)


def test_no_trailing_comma(fixer):
    b = """print >>sys.stderr, 1+1"""
    a = """print(1+1, file=sys.stderr)"""
    fixer.check(b, a)


def test_spaces_before_file(fixer):
    b = """print >>  sys.stderr"""
    a = """print(file=sys.stderr)"""
    fixer.check(b, a)


def test_with_future_print_function(fixer):
    s = "from __future__ import print_function\n" "print('Hai!', end=' ')"
    fixer.unchanged(s)

    b = "print 'Hello, world!'"
    a = "print('Hello, world!')"
    fixer.check(b, a)
