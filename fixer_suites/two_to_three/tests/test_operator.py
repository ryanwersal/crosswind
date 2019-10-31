import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(two_to_three_test_case):
    return two_to_three_test_case("operator")


def test_operator_isCallable(fixer):
    b = "operator.isCallable(x)"
    a = "callable(x)"
    fixer.check(b, a)


def test_operator_sequenceIncludes(fixer):
    b = "operator.sequenceIncludes(x, y)"
    a = "operator.contains(x, y)"
    fixer.check(b, a)

    b = "operator .sequenceIncludes(x, y)"
    a = "operator .contains(x, y)"
    fixer.check(b, a)

    b = "operator.  sequenceIncludes(x, y)"
    a = "operator.  contains(x, y)"
    fixer.check(b, a)


def test_operator_isSequenceType(fixer):
    b = "operator.isSequenceType(x)"
    a = "import collections.abc\nisinstance(x, collections.abc.Sequence)"
    fixer.check(b, a)


def test_operator_isMappingType(fixer):
    b = "operator.isMappingType(x)"
    a = "import collections.abc\nisinstance(x, collections.abc.Mapping)"
    fixer.check(b, a)


def test_operator_isNumberType(fixer):
    b = "operator.isNumberType(x)"
    a = "import numbers\nisinstance(x, numbers.Number)"
    fixer.check(b, a)


def test_operator_repeat(fixer):
    b = "operator.repeat(x, n)"
    a = "operator.mul(x, n)"
    fixer.check(b, a)

    b = "operator .repeat(x, n)"
    a = "operator .mul(x, n)"
    fixer.check(b, a)

    b = "operator.  repeat(x, n)"
    a = "operator.  mul(x, n)"
    fixer.check(b, a)


def test_operator_irepeat(fixer):
    b = "operator.irepeat(x, n)"
    a = "operator.imul(x, n)"
    fixer.check(b, a)

    b = "operator .irepeat(x, n)"
    a = "operator .imul(x, n)"
    fixer.check(b, a)

    b = "operator.  irepeat(x, n)"
    a = "operator.  imul(x, n)"
    fixer.check(b, a)


def test_bare_isCallable(fixer):
    s = "isCallable(x)"
    t = "You should use 'callable(x)' here."
    fixer.warns_unchanged(s, t)


def test_bare_sequenceIncludes(fixer):
    s = "sequenceIncludes(x, y)"
    t = "You should use 'operator.contains(x, y)' here."
    fixer.warns_unchanged(s, t)


def test_bare_operator_isSequenceType(fixer):
    s = "isSequenceType(z)"
    t = "You should use 'isinstance(z, collections.abc.Sequence)' here."
    fixer.warns_unchanged(s, t)


def test_bare_operator_isMappingType(fixer):
    s = "isMappingType(x)"
    t = "You should use 'isinstance(x, collections.abc.Mapping)' here."
    fixer.warns_unchanged(s, t)


def test_bare_operator_isNumberType(fixer):
    s = "isNumberType(y)"
    t = "You should use 'isinstance(y, numbers.Number)' here."
    fixer.warns_unchanged(s, t)


def test_bare_operator_repeat(fixer):
    s = "repeat(x, n)"
    t = "You should use 'operator.mul(x, n)' here."
    fixer.warns_unchanged(s, t)


def test_bare_operator_irepeat(fixer):
    s = "irepeat(y, 187)"
    t = "You should use 'operator.imul(y, 187)' here."
    fixer.warns_unchanged(s, t)
