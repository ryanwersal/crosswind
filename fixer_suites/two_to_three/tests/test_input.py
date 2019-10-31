from crosswind.tests.support import FixerTestCase


class Test_input(FixerTestCase):
    fixer = "input"

    def test_prefix_preservation(self):
        b = """x =   input(   )"""
        a = """x =   eval(input(   ))"""
        self.check(b, a)

        b = """x = input(   ''   )"""
        a = """x = eval(input(   ''   ))"""
        self.check(b, a)

    def test_trailing_comment(self):
        b = """x = input()  #  foo"""
        a = """x = eval(input())  #  foo"""
        self.check(b, a)

    def test_idempotency(self):
        s = """x = eval(input())"""
        self.unchanged(s)

        s = """x = eval(input(''))"""
        self.unchanged(s)

        s = """x = eval(input(foo(5) + 9))"""
        self.unchanged(s)

    def test_1(self):
        b = """x = input()"""
        a = """x = eval(input())"""
        self.check(b, a)

    def test_2(self):
        b = """x = input('')"""
        a = """x = eval(input(''))"""
        self.check(b, a)

    def test_3(self):
        b = """x = input('prompt')"""
        a = """x = eval(input('prompt'))"""
        self.check(b, a)

    def test_4(self):
        b = """x = input(foo(5) + 9)"""
        a = """x = eval(input(foo(5) + 9))"""
        self.check(b, a)
