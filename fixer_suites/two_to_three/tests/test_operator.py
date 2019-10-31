from crosswind.tests.support import FixerTestCase


class Test_operator(FixerTestCase):

    fixer = "operator"

    def test_operator_isCallable(self):
        b = "operator.isCallable(x)"
        a = "callable(x)"
        self.check(b, a)

    def test_operator_sequenceIncludes(self):
        b = "operator.sequenceIncludes(x, y)"
        a = "operator.contains(x, y)"
        self.check(b, a)

        b = "operator .sequenceIncludes(x, y)"
        a = "operator .contains(x, y)"
        self.check(b, a)

        b = "operator.  sequenceIncludes(x, y)"
        a = "operator.  contains(x, y)"
        self.check(b, a)

    def test_operator_isSequenceType(self):
        b = "operator.isSequenceType(x)"
        a = "import collections.abc\nisinstance(x, collections.abc.Sequence)"
        self.check(b, a)

    def test_operator_isMappingType(self):
        b = "operator.isMappingType(x)"
        a = "import collections.abc\nisinstance(x, collections.abc.Mapping)"
        self.check(b, a)

    def test_operator_isNumberType(self):
        b = "operator.isNumberType(x)"
        a = "import numbers\nisinstance(x, numbers.Number)"
        self.check(b, a)

    def test_operator_repeat(self):
        b = "operator.repeat(x, n)"
        a = "operator.mul(x, n)"
        self.check(b, a)

        b = "operator .repeat(x, n)"
        a = "operator .mul(x, n)"
        self.check(b, a)

        b = "operator.  repeat(x, n)"
        a = "operator.  mul(x, n)"
        self.check(b, a)

    def test_operator_irepeat(self):
        b = "operator.irepeat(x, n)"
        a = "operator.imul(x, n)"
        self.check(b, a)

        b = "operator .irepeat(x, n)"
        a = "operator .imul(x, n)"
        self.check(b, a)

        b = "operator.  irepeat(x, n)"
        a = "operator.  imul(x, n)"
        self.check(b, a)

    def test_bare_isCallable(self):
        s = "isCallable(x)"
        t = "You should use 'callable(x)' here."
        self.warns_unchanged(s, t)

    def test_bare_sequenceIncludes(self):
        s = "sequenceIncludes(x, y)"
        t = "You should use 'operator.contains(x, y)' here."
        self.warns_unchanged(s, t)

    def test_bare_operator_isSequenceType(self):
        s = "isSequenceType(z)"
        t = "You should use 'isinstance(z, collections.abc.Sequence)' here."
        self.warns_unchanged(s, t)

    def test_bare_operator_isMappingType(self):
        s = "isMappingType(x)"
        t = "You should use 'isinstance(x, collections.abc.Mapping)' here."
        self.warns_unchanged(s, t)

    def test_bare_operator_isNumberType(self):
        s = "isNumberType(y)"
        t = "You should use 'isinstance(y, numbers.Number)' here."
        self.warns_unchanged(s, t)

    def test_bare_operator_repeat(self):
        s = "repeat(x, n)"
        t = "You should use 'operator.mul(x, n)' here."
        self.warns_unchanged(s, t)

    def test_bare_operator_irepeat(self):
        s = "irepeat(y, 187)"
        t = "You should use 'operator.imul(y, 187)' here."
        self.warns_unchanged(s, t)
