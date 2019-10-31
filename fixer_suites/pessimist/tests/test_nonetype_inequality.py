import pytest


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


@pytest.fixture(name="fixer")
def fixer_fixture(pessimist_test_case):
    return pessimist_test_case("nonetype_inequality")


def test_adds_none_check_for_greater_than_on_left(fixer):
    b = """if foo > 5: pass"""
    a = """if foo is not None and foo > 5: pass"""
    fixer.check(b, a)


def test_adds_none_check_for_greater_than_on_right(fixer):
    b = """if 5 < foo: pass"""
    a = """if foo is not None and 5 < foo: pass"""
    fixer.check(b, a)


def test_adds_none_check_for_less_than_on_left(fixer):
    b = """if foo < 5: pass"""
    a = """if foo is None or foo < 5: pass"""
    fixer.check(b, a)


def test_adds_none_check_for_less_than_on_right(fixer):
    b = """if 5 > foo: pass"""
    a = """if foo is None or 5 > foo: pass"""
    fixer.check(b, a)
