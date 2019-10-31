import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(two_to_three_test_case):
    return two_to_three_test_case("nonzero")


def test_1(fixer):
    b = """
        class A:
            def __nonzero__(self):
                pass
        """
    a = """
        class A:
            def __bool__(self):
                pass
        """
    fixer.check(b, a)


def test_2(fixer):
    b = """
        class A(object):
            def __nonzero__(self):
                pass
        """
    a = """
        class A(object):
            def __bool__(self):
                pass
        """
    fixer.check(b, a)


def test_unchanged_1(fixer):
    s = """
        class A(object):
            def __bool__(self):
                pass
        """
    fixer.unchanged(s)


def test_unchanged_2(fixer):
    s = """
        class A(object):
            def __nonzero__(self, a):
                pass
        """
    fixer.unchanged(s)


def test_unchanged_func(fixer):
    s = """
        def __nonzero__(self):
            pass
        """
    fixer.unchanged(s)
