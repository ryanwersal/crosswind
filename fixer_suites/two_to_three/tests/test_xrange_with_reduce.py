from .util import FixerTestCase


class Test_xrange_with_reduce(FixerTestCase):
    def setUp(self):
        super(Test_xrange_with_reduce, self).setUp(["xrange", "reduce"])

    def test_double_transform(self):
        b = """reduce(x, xrange(5))"""
        a = """from functools import reduce
reduce(x, range(5))"""
        self.check(b, a)
