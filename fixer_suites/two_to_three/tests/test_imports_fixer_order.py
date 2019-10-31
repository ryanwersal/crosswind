from crosswind.tests.support import FixerTestCase

from .util import ImportsFixerTests


class Test_imports_fixer_order(FixerTestCase, ImportsFixerTests):
    def setUp(self):
        super(Test_imports_fixer_order, self).setUp(["imports", "imports2"])
        from ..fixes.fix_imports2 import MAPPING as mapping2

        self.modules = mapping2.copy()
        from ..fixes.fix_imports import MAPPING as mapping1

        for key in ("dbhash", "dumbdbm", "dbm", "gdbm"):
            self.modules[key] = mapping1[key]

    def test_after_local_imports_refactoring(self):
        for fix in ("imports", "imports2"):
            self.fixer = fix
            self.assert_runs_after("import")
