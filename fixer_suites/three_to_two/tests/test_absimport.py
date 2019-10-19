from .support import crosswindFixerTestCase


class Test_absimport(crosswindFixerTestCase):
    fixer = "absimport"

    def test_import(self):
        a = "import abc"
        b = "from __future__ import absolute_import\nimport abc"

        self.check(a, b)

    def test_no_imports(self):
        a = "2+2"

        self.unchanged(a)
