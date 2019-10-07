from crosswind.tests.support import crosswindFixerTestCase

class Test_memoryview(crosswindFixerTestCase):
    fixer = "memoryview"

    def test_simple(self):
        b = """x = memoryview(y)"""
        a = """x = buffer(y)"""
        self.check(b, a)

    def test_slicing(self):
        b = """x = memoryview(y)[1:4]"""
        a = """x = buffer(y)[1:4]"""
        self.check(b, a)

    def test_prefix_preservation(self):
        b = """x =       memoryview(  y )[1:4]"""
        a = """x =       buffer(  y )[1:4]"""
        self.check(b, a)

    def test_nested(self):
        b = """x = list(memoryview(y)[1:4])"""
        a = """x = list(buffer(y)[1:4])"""
        self.check(b, a)
