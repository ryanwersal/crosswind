"""
Remove builtins imports
from builtins import foo is replaced with an empty line.
"""
from crosswind import fixer_base
from crosswind.fixer_util import BlankLine


class FixBuiltins(fixer_base.BaseFix):
    BM_compatible = True

    PATTERN = r"""
        import_from< 'from' 'builtins' 'import' any >
        |
        import_from<
            'from' dotted_name<'future' '.' 'builtins'> 'import' any
        >
    """

    def transform(self, node, results):
        new = BlankLine()
        new.prefix = node.prefix
        return new
