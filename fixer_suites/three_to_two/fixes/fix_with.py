"""
Fixer for from __future__ import with_statement
"""

from crosswind import fixer_base
from crosswind.fixer_util_3to2 import future_import


class FixWith(fixer_base.BaseFix):

    PATTERN = "with_stmt"

    def transform(self, node, results):
        future_import("with_statement", node)
