"""
Fixer for division: from __future__ import division if needed
"""

from crosswind import fixer_base
from crosswind.fixer_util_3to2 import future_import, token


def match_division(node):
    """
    __future__.division redefines the meaning of a single slash for division,
    so we match that and only that.
    """
    slash = token.SLASH
    return node.type == slash and not node.next_sibling.type == slash and not node.prev_sibling.type == slash


class FixDivision(fixer_base.BaseFix):
    def match(self, node):
        """
        Since the tree needs to be fixed once and only once if and only if it
        matches, then we can start discarding matches after we make the first.
        """
        return match_division(node)

    def transform(self, node, results):
        future_import("division", node)
