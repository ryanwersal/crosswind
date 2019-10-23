"""
Fixer for open(...) -> io.open(...)
"""

from crosswind import fixer_base
from crosswind.fixer_util import is_probably_builtin, touch_import


class FixOpen(fixer_base.BaseFix):

    PATTERN = """'open'"""

    def transform(self, node, results):

        if is_probably_builtin(node):
            touch_import("io", "open", node)
