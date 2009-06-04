"""Fixer that turns 'int' into 'long' everywhere.
"""

from lib2to3 import fixer_base
from lib2to3.fixer_util import Name, is_probably_builtin


class FixInt(fixer_base.BaseFix):

    PATTERN = "'int'"

    static_long = Name(u"long")

    def transform(self, node, results):
        if is_probably_builtin(node):
            new = self.static_long.clone()
            new.prefix = node.prefix
            return new
