"""
Fixer for print: from __future__ import print_function.
"Placeholder": In the future, this will transform print into a print statement
"""

from lib2to3 import fixer_base, pytree
from lib2to3.fixer_util import (Name, Comma, FromImport, touch_import, Newline,
                                is_probably_builtin)
from lib2to3.pgen2 import token

class FixPrint(fixer_base.BaseFix):

    def start_tree(self, tree, filename):
        """This is only run once; we want to remember the first node"""
        super(FixPrint, self).start_tree(tree, filename)
        self._tree = tree
    
    PATTERN = """
              power< 'print' trailer < '(' any* ')' > any* >
              """
    
    def match(self, node):
        """
        Since the tree needs to be fixed once and only once if and only if it
        matches, then we can start discarding matches after we make the first.
        """
        return not 'print_happened' in dir(self._tree) and super(FixPrint,self).match(node)

    def transform(self, node, results):
        tree = self._tree
        syms = self.syms
        tree.print_happened = True
        future_stmt = FromImport(u"__future__",
                                [pytree.Leaf(token.NAME, u"print_function",
                                prefix=u" ")])
        children = list(tree.children[:])
        for child in children:
            child.remove()
        children = [future_stmt, Newline()] + children
        newnode = pytree.Node(syms.simple_stmt, children)
        tree.insert_child(0, newnode)
