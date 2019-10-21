from .util import FixerTestCase


class Test_raw_input(FixerTestCase):
    fixer = "raw_input"

    def test_prefix_preservation(self):
        b = """x =    raw_input(   )"""
        a = """x =    input(   )"""
        self.check(b, a)

        b = """x = raw_input(   ''   )"""
        a = """x = input(   ''   )"""
        self.check(b, a)

    def test_1(self):
        b = """x = raw_input()"""
        a = """x = input()"""
        self.check(b, a)

    def test_2(self):
        b = """x = raw_input('')"""
        a = """x = input('')"""
        self.check(b, a)

    def test_3(self):
        b = """x = raw_input('prompt')"""
        a = """x = input('prompt')"""
        self.check(b, a)

    def test_4(self):
        b = """x = raw_input(foo(a) + 6)"""
        a = """x = input(foo(a) + 6)"""
        self.check(b, a)

    def test_5(self):
        b = """x = raw_input(invite).split()"""
        a = """x = input(invite).split()"""
        self.check(b, a)

    def test_6(self):
        b = """x = raw_input(invite) . split ()"""
        a = """x = input(invite) . split ()"""
        self.check(b, a)

    def test_8(self):
        b = "x = int(raw_input())"
        a = "x = int(input())"
        self.check(b, a)
