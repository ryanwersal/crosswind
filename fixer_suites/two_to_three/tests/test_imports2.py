from crosswind.tests.support import FixerTestCase

from .util import ImportsFixerTests


class Test_imports2(FixerTestCase, ImportsFixerTests):
    fixer = "imports2"
    from ..fixes.fix_imports2 import MAPPING as modules
