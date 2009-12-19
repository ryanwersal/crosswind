from test_all_fixers import lib3to2FixerTestCase

class Test_imports_test(lib3to2FixerTestCase):
    fixer = "imports_test"

    def test_submods(self):
        b = "from http import client,"
        a = "import httplib as client"
        self.check(b, a)
