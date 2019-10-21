from .support import crosswindFixerTestCase


class Test_getcwd(crosswindFixerTestCase):
    fixer = "getcwd"

    def test_prefix_preservation(self):
        b = """ls =    os.listdir(  os.getcwd()  )"""
        a = """ls =    os.listdir(  os.getcwdu()  )"""
        self.check(b, a)

        b = """whatdir = os.getcwd      (      )"""
        a = """whatdir = os.getcwdu      (      )"""
        self.check(b, a)
