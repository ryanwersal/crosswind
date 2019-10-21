from .util import FixerTestCase


class Test_reduce(FixerTestCase):
    fixer = "reduce"

    def test_simple_call(self):
        b = "reduce(a, b, c)"
        a = "from functools import reduce\nreduce(a, b, c)"
        self.check(b, a)

    def test_bug_7253(self):
        # fix_tuple_params was being bad and orphaning nodes in the tree.
        b = "def x(arg): reduce(sum, [])"
        a = "from functools import reduce\ndef x(arg): reduce(sum, [])"
        self.check(b, a)

    def test_call_with_lambda(self):
        b = "reduce(lambda x, y: x + y, seq)"
        a = "from functools import reduce\nreduce(lambda x, y: x + y, seq)"
        self.check(b, a)

    def test_unchanged(self):
        s = "reduce(a)"
        self.unchanged(s)

        s = "reduce(a, b=42)"
        self.unchanged(s)

        s = "reduce(a, b, c, d)"
        self.unchanged(s)

        s = "reduce(**c)"
        self.unchanged(s)

        s = "reduce()"
        self.unchanged(s)
