import pytest

from crosswind.tests.support import FixerTestCase
from fixer_suites.two_to_three.tests import util


def test_none_less_than_value_throws():
    with pytest.raises(TypeError) as ex:
        _ = None < 5
    assert "'<' not supported between instances" in str(ex.value)


def test_none_less_than_equal_value_throws():
    with pytest.raises(TypeError) as ex:
        _ = None <= 5
    assert "'<=' not supported between instances" in str(ex.value)


def test_none_greater_than_value_throws():
    with pytest.raises(TypeError) as ex:
        _ = None > 5
    assert "'>' not supported between instances" in str(ex.value)


def test_none_greater_than_equal_value_throws():
    with pytest.raises(TypeError) as ex:
        _ = None >= 5
    assert "'>=' not supported between instances" in str(ex.value)


def test_none_equal_to_does_not_throw():
    assert not None == 5  # pylint: disable=singleton-comparison


def test_none_is_does_not_throw():
    assert not None is 5  # pylint: disable=literal-comparison


@pytest.fixture(name="pessimist")
def pessimist_fixture():
    test_case = FixerTestCase()
    test_case.fixer = "nonetype_inequality"
    test_case.setUp(fixer_pkg="fixer_suites.pessimist")
    yield test_case


def test_adds_none_check_for_greater_than_on_left(pessimist):
    b = """if foo > 5: pass"""
    a = """if foo is not None and foo > 5: pass"""
    pessimist.check(b, a)


def test_adds_none_check_for_greater_than_on_right(pessimist):
    b = """if 5 < foo: pass"""
    a = """if foo is not None and 5 < foo: pass"""
    pessimist.check(b, a)


def test_adds_none_check_for_less_than_on_left(pessimist):
    b = """if foo < 5: pass"""
    a = """if foo is None or foo < 5: pass"""
    pessimist.check(b, a)


def test_adds_none_check_for_less_than_on_right(pessimist):
    b = """if 5 > foo: pass"""
    a = """if foo is None or 5 > foo: pass"""
    pessimist.check(b, a)
