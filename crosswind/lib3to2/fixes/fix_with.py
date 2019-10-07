"""
Fixer for from __future__ import with_statement
"""

from crosswind.lib2to3 import fixer_base
from crosswind.lib3to2.fixer_util import future_import

class FixWith(fixer_base.BaseFix):

    PATTERN = "with_stmt"

    def transform(self, node, results):
        future_import("with_statement", node)
