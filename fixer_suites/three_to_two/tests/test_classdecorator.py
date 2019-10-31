import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(three_to_two_test_case):
    return three_to_two_test_case("classdecorator")


def test_basic_functionality(fixer):

    b = """
    @decor
    class decorated(object):
        pass"""

    a = """
    class decorated(object):
        pass
    decorated = decor(decorated)"""

    fixer.check(b, a)


def test_whitespace(fixer):

    b = """
    @decor
    class decorated(object):
        pass
    print("hello, there!")"""

    a = """
    class decorated(object):
        pass
    decorated = decor(decorated)

    print("hello, there!")"""

    fixer.check(b, a)


def test_chained(fixer):

    b = """
    @f1
    @f2
    @f3
    class wow(object):
        do_cool_stuff_here()"""

    a = """
    class wow(object):
        do_cool_stuff_here()
    wow = f1(f2(f3(wow)))"""

    fixer.check(b, a)


def test_dots_and_parens(fixer):

    b = """
    @should_work.with_dots(and_parens)
    @dotted.name
    @with_args(in_parens)
    class awesome(object):
        inconsequential_stuff()"""

    a = """
    class awesome(object):
        inconsequential_stuff()
    awesome = should_work.with_dots(and_parens)(dotted.name(with_args(in_parens)(awesome)))"""

    fixer.check(b, a)


def test_indentation(fixer):

    b = """
    if 1:
        if 2:
            if 3:
                @something
                @something_else
                class foo(bar):
                    do_stuff()
            elif 4:
                pass"""
    a = """
    if 1:
        if 2:
            if 3:
                class foo(bar):
                    do_stuff()
                foo = something(something_else(foo))
            elif 4:
                pass"""

    # FIXME: This was lacking an assert and it doesn't appear to work so need to figure that out.
    # fixer.check(b, a)
