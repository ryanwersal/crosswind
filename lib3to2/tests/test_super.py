from lib3to2.tests.support import lib3to2FixerTestCase

class Test_super(lib3to2FixerTestCase):
    fixer = "super"

    def test_noargs(self):

        b = "def m(self):\n    super()"
        a = "def m(self):\n    super(self.__class__, self)"
        self.check(b, a)

    def test_other_params(self):

        b = "def m(a, self=None):\n    super()"
        a = "def m(a, self=None):\n    super(a.__class__, a)"
        self.check(b, a)

    def test_no_with_stars(self):

        s = "def m(*args, **kwargs):\n    super()"
        self.unchanged(s, ignore_warnings=True)

    def test_no_with_noargs(self):

        s = "def m():\n    super()"
        self.unchanged(s, ignore_warnings=True)
