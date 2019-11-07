"""Remove from io import open"""
from crosswind import fixer_base
from crosswind.fixer_util import BlankLine


class FixOpen(fixer_base.BaseFix):
    BM_compatible = True

    PATTERN = r"import_from< 'from' 'io' 'import' 'open' >"

    def transform(self, node, results):
        new = BlankLine()
        new.prefix = node.prefix
        return new
