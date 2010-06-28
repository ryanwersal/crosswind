from test_all_fixers import lib3to2FixerTestCase

class Test_super(lib3to2FixerTestCase):
    fixer = "super"

    def test_noargs(self):

        b = "def m(self):\n    super()"
        a = "def m(self):\n    super(self.__class__, self)"
        self.check(b, a)
