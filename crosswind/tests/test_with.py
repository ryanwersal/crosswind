from crosswind.tests.support import crosswindFixerTestCase

class Test_with(crosswindFixerTestCase):
    fixer = "with"

    def test_with_oneline(self):
        b = "with a as b: pass"
        a = "from __future__ import with_statement\nwith a as b: pass"
        self.check(b, a)

    def test_with_suite(self):
        b = "with a as b:\n    pass"
        a = "from __future__ import with_statement\nwith a as b:\n    pass"
        self.check(b, a)
