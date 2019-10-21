from .util import FixerTestCase


class Test_sys_exc(FixerTestCase):
    fixer = "sys_exc"

    def test_0(self):
        b = "sys.exc_type"
        a = "sys.exc_info()[0]"
        self.check(b, a)

    def test_1(self):
        b = "sys.exc_value"
        a = "sys.exc_info()[1]"
        self.check(b, a)

    def test_2(self):
        b = "sys.exc_traceback"
        a = "sys.exc_info()[2]"
        self.check(b, a)

    def test_3(self):
        b = "sys.exc_type # Foo"
        a = "sys.exc_info()[0] # Foo"
        self.check(b, a)

    def test_4(self):
        b = "sys.  exc_type"
        a = "sys.  exc_info()[0]"
        self.check(b, a)

    def test_5(self):
        b = "sys  .exc_type"
        a = "sys  .exc_info()[0]"
        self.check(b, a)
