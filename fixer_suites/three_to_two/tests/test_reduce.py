import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(three_to_two_test_case):
    return three_to_two_test_case("reduce")


def test_functools_import(fixer):

    b = """
        from functools import reduce
        reduce(f, it)"""
    a = """
        reduce(f, it)"""
    fixer.check(b, a)

    b = """
        do_other_stuff; from functools import reduce
        reduce(f, it)"""
    a = """
        do_other_stuff
        reduce(f, it)"""
    fixer.check(b, a)

    b = """
        do_other_stuff; from functools import reduce; do_more_stuff
        reduce(f, it)"""
    a = """
        do_other_stuff; do_more_stuff
        reduce(f, it)"""
    fixer.check(b, a)


def test_functools_reduce(fixer):

    b = """
        import functools
        functools.reduce(spam, ['spam', 'spam', 'baked beans', 'spam'])
        """
    a = """
        import functools
        reduce(spam, ['spam', 'spam', 'baked beans', 'spam'])
        """
    fixer.check(b, a)


def test_prefix(fixer):

    b = """
        a  =  functools.reduce( self.thing,  self.children , f( 3 ))
        """
    a = """
        a  =  reduce( self.thing,  self.children , f( 3 ))
        """
    fixer.check(b, a)
