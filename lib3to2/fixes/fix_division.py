"""
Fixer for division: from __future__ import division if needed
"""

from lib2to3 import fixer_base, pytree
from lib2to3.fixer_util import (Name, Comma, FromImport, touch_import, Newline,
                                is_probably_builtin)
from lib2to3.pgen2 import token

def match_division(node):
    """
    __future__.division redefines the meaning of a single slash for division,
    so we match that and only that.
    """
    slash = token.SLASH
    return node.type == slash and not node.next_sibling.type == slash and \
                                  not node.prev_sibling.type == slash

class FixDivision(fixer_base.BaseFix):

    def start_tree(self, tree, filename):
        """This is only run once; we want to remember the first node"""
        super(FixDivision, self).start_tree(tree, filename)
        self._tree = tree
    
    def match(self, node):
        """
        Since the tree needs to be fixed once and only once if and only if it
        matches, then we can start discarding matches after we make the first.
        """
        return not 'div_happened' in dir(self._tree) and match_division(node)

    def transform(self, node, results):
        tree = self._tree
        tree.div_happened = True
        syms = self.syms
        future_stmt = FromImport(u"__future__",
                                [pytree.Leaf(token.NAME, u"division",
                                prefix=u" ")])
        children = list(tree.children[:])
        new_node = pytree.Node(syms.simple_stmt, [future_stmt, Newline()])
        for child in children:
            child.remove()
            new_node.append_child(child)
        tree.insert_child(0, new_node)
