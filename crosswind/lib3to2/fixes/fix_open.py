"""
Fixer for open(...) -> io.open(...)
"""

from crosswind.lib2to3 import fixer_base
from crosswind.lib2to3.fixer_util import touch_import, is_probably_builtin


class FixOpen(fixer_base.BaseFix):

    PATTERN = """'open'"""

    def transform(self, node, results):

        if is_probably_builtin(node):
            touch_import("io", "open", node)
