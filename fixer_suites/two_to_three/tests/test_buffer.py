from .util import FixerTestCase


class Test_buffer(FixerTestCase):
    fixer = "buffer"

    def test_buffer(self):
        b = """x = buffer(y)"""
        a = """x = memoryview(y)"""
        self.check(b, a)

    def test_slicing(self):
        b = """buffer(y)[4:5]"""
        a = """memoryview(y)[4:5]"""
        self.check(b, a)
