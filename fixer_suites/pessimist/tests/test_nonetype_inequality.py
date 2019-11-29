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


def test_adds_none_check_for_greater_than_equal_to_on_left(fixer):
    b = """if foo >= 5: pass"""
    a = """if foo is not None and foo >= 5: pass"""
    fixer.check(b, a)


def test_adds_none_check_for_greater_than_on_right(fixer):
    b = """if 5 < foo: pass"""
    a = """if foo is not None and 5 < foo: pass"""
    fixer.check(b, a)


def test_adds_none_check_for_greater_than_equal_on_right(fixer):
    b = """if 5 <= foo: pass"""
    a = """if foo is not None and 5 <= foo: pass"""
    fixer.check(b, a)


def test_adds_none_check_for_less_than_on_left(fixer):
    b = """if foo < 5: pass"""
    a = """if foo is None or foo < 5: pass"""
    fixer.check(b, a)


def test_adds_none_check_for_less_than_equal_on_left(fixer):
    b = """if foo <= 5: pass"""
    a = """if foo is None or foo <= 5: pass"""
    fixer.check(b, a)


def test_adds_none_check_for_less_than_on_right(fixer):
    b = """if 5 > foo: pass"""
    a = """if foo is None or 5 > foo: pass"""
    fixer.check(b, a)


def test_adds_none_check_for_less_than_equal_on_right(fixer):
    b = """if 5 >= foo: pass"""
    a = """if foo is None or 5 >= foo: pass"""
    fixer.check(b, a)


def test_unchanged_if_is_not_operator(fixer):
    u = """if foo is not None: pass"""
    fixer.unchanged(u)


def test_unchanged_if_pattern_not_found(fixer):
    u = """print('foo')"""
    fixer.unchanged(u)


SYMBOLS = ["<", ">", "<=", ">="]
LOGICAL_OP = ["and", "or"]


@pytest.mark.parametrize("symbol", SYMBOLS)
def test_unchanged_if_inequality_involves_names_on_both_sides(fixer, symbol):
    u = f"if foo {symbol} bar: pass"
    fixer.warns_unchanged(u, "Inequality between two names is unhandled and can only be manually inspected.")


@pytest.mark.parametrize("symbol", SYMBOLS)
def test_unchanged_if_parenthized(fixer, symbol):
    u = f"if (foo {symbol} 5): pass"
    fixer.unchanged(u)


@pytest.mark.parametrize("symbol,logic", [(x, y) for x in SYMBOLS for y in LOGICAL_OP])
def test_unchanged_if_inequality_already_part_of_complex_logical(fixer, symbol, logic):
    u = f"if foo {symbol} 5 {logic} something is None: pass"
    fixer.unchanged(u)

    u = f"if something is None {logic} foo {symbol} 5: pass"
    fixer.unchanged(u)

    u = f"if bar >= 10 {logic} foo {symbol} 5: pass"
    fixer.unchanged(u)
