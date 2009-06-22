"""
Fixer for except E as T -> except E, T
"""

from lib2to3 import fixer_base
from lib2to3.fixer_util import Comma
from lib2to3.pytree import Leaf

class FixExcept(fixer_base.BaseFix):

    PATTERN = """except_clause< 'except' any 'as' any >"""

    def transform(self, node, results):
        for child in node.children:
            if child == Leaf(1, u"as"):
                i = child.remove()
                node.insert_child(i, Comma())
