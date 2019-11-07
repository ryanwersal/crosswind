"""Fixer for future.standard_library"""
from crosswind import fixer_base
from crosswind.fixer_util import BlankLine


class FixStandardLibrary(fixer_base.BaseFix):
    BM_compatible = True

    PATTERN = r"""
        power<
            'standard_library' trailer< '.' 'install_aliases' >
            trailer< '(' ')' >
        >
        |
        import_from< 'from' 'future' 'import' 'standard_library' >
      """

    def transform(self, node, results):
        new = BlankLine()
        new.prefix = node.prefix
        return new
