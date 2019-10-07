from crosswind.tests.support import crosswindFixerTestCase

class Test_newstyle(crosswindFixerTestCase):
    fixer = "newstyle"

    def test_oneline(self):

        b = """class Foo: pass"""
        a = """class Foo(object): pass"""
        self.check(b, a)

    def test_suite(self):

        b = """
        class Foo():
            do_stuff()"""
        a = """
        class Foo(object):
            do_stuff()"""
        self.check(b, a)

