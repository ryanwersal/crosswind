import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(three_to_two_test_case):
    return three_to_two_test_case("bool")


def test_1(fixer):
    b = """
        class A:
            def __bool__(self):
                pass
        """
    a = """
        class A:
            def __nonzero__(self):
                pass
        """
    fixer.check(b, a)


def test_2(fixer):
    b = """
        class A(object):
            def __bool__(self):
                pass
        """
    a = """
        class A(object):
            def __nonzero__(self):
                pass
        """
    fixer.check(b, a)


def test_unchanged_1(fixer):
    s = """
        class A(object):
            def __nonzero__(self):
                pass
        """
    fixer.unchanged(s)


def test_unchanged_2(fixer):
    s = """
        class A(object):
            def __bool__(self, a):
                pass
        """
    fixer.unchanged(s)


def test_unchanged_func(fixer):
    s = """
        def __bool__(thing):
            pass
        """
    fixer.unchanged(s)
