from lib3to2.tests.support import lib3to2FixerTestCase

class Test_newstyle(lib3to2FixerTestCase):
    fixer = u"newstyle"

    def test_oneline(self):

        b = u"""class Foo: pass"""
        a = u"""class Foo(object): pass"""
        self.check(b, a)

    def test_suite(self):

        b = u"""
        class Foo():
            do_stuff()"""
        a = u"""
        class Foo(object):
            do_stuff()"""
        self.check(b, a)

