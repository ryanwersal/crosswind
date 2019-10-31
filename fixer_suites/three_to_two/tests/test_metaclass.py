import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(three_to_two_test_case):
    return three_to_two_test_case("metaclass")


def test_unchanged(fixer):
    fixer.unchanged("class X(): pass")
    fixer.unchanged("class X(object): pass")
    fixer.unchanged("class X(object1, object2): pass")
    fixer.unchanged("class X(object1, object2, object3): pass")

    s = """
    class X():
        def __metaclass__(fixer): pass
    """
    fixer.unchanged(s)

    s = """
    class X():
        a[23] = 74
    """
    fixer.unchanged(s)


def test_comments(fixer):
    a = """
    class X(object):
        # hi
        __metaclass__ = AppleMeta
        pass
    """
    b = """
    class X(metaclass=AppleMeta):
        # hi
        pass
    """
    fixer.check(b, a)

    a = """
    class X(object):
        __metaclass__ = Meta
        pass
        # Bedtime!
    """
    b = """
    class X(metaclass=Meta):
        pass
        # Bedtime!
    """
    fixer.check(b, a)


def test_meta_noparent_odd_body(fixer):
    # no-parent class, odd body
    a = """
    class X(object):
        __metaclass__ = Q
        pass
    """
    b = """
    class X(metaclass=Q):
        pass
    """
    fixer.check(b, a)


def test_meta_oneparent_no_body(fixer):
    # one parent class, no body
    a = """
    class X(object):
        __metaclass__ = Q
        pass"""
    b = """
    class X(object, metaclass=Q): pass"""
    fixer.check(b, a)


def test_meta_oneparent_simple_body_1(fixer):
    # one parent, simple body
    a = """
    class X(object):
        __metaclass__ = Meta
        bar = 7
    """
    b = """
    class X(object, metaclass=Meta):
        bar = 7
    """
    fixer.check(b, a)


def test_meta_oneparent_simple_body_2(fixer):
    a = """
    class X(object):
        __metaclass__ = Meta
        x = 4; g = 23
    """
    b = """
    class X(metaclass=Meta):
        x = 4; g = 23
    """
    fixer.check(b, a)


def test_meta_oneparent_simple_body_3(fixer):
    a = """
    class X(object):
        __metaclass__ = Meta
        bar = 7
    """
    b = """
    class X(object, metaclass=Meta):
        bar = 7
    """
    fixer.check(b, a)


def test_meta_multiparent_simple_body_1(fixer):
    # multiple inheritance, simple body
    a = """
    class X(clsA, clsB):
        __metaclass__ = Meta
        bar = 7
    """
    b = """
    class X(clsA, clsB, metaclass=Meta):
        bar = 7
    """
    fixer.check(b, a)


def test_meta_multiparent_simple_body_2(fixer):
    # keywords in the class statement
    a = """
    class m(a, arg=23):
        __metaclass__ = Meta
        pass"""
    b = """
    class m(a, arg=23, metaclass=Meta):
        pass"""
    fixer.check(b, a)


def test_meta_expression_simple_body_1(fixer):
    a = """
    class X(expression(2 + 4)):
        __metaclass__ = Meta
        pass
    """
    b = """
    class X(expression(2 + 4), metaclass=Meta):
        pass
    """
    fixer.check(b, a)


def test_meta_expression_simple_body_2(fixer):
    a = """
    class X(expression(2 + 4), x**4):
        __metaclass__ = Meta
        pass
    """
    b = """
    class X(expression(2 + 4), x**4, metaclass=Meta):
        pass
    """
    fixer.check(b, a)


def test_meta_noparent_simple_body(fixer):

    a = """
    class X(object):
        __metaclass__ = Meta
        save.py = 23
        out = 5
    """
    b = """
    class X(metaclass=Meta):
        save.py = 23
        out = 5
    """
    fixer.check(b, a)
