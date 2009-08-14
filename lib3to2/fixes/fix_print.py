"""
Fixer for print: from __future__ import print_function.
"Placeholder": In the future, this will transform print into a print statement
"""

from lib2to3 import fixer_base
from lib2to3.pytree import Node
from lib2to3.fixer_util import Name, FromImport, Newline

class FixPrint(fixer_base.BaseFix):

    def start_tree(self, tree, filename):
        """This is only run once; we want to remember the first node"""
        super(FixPrint, self).start_tree(tree, filename)
        self._tree = tree
        self.have_print = False

    PATTERN = """
              power< 'print' trailer < '(' any* ')' > any* >
              """

    def match(self, node):
        """
        Since the tree needs to be fixed once and only once if and only if it
        matches, then we can start discarding matches after we make the first.
        """
        return not self.have_print and super(FixPrint,self).match(node)

    def transform(self, node, results):
        tree = self._tree
        self.have_print = True
        syms = self.syms
        future_stmt = FromImport(u"__future__",
                                [Name(u"print_function", prefix=u" ")])
        children = tree.children[:]
        new_node = Node(syms.simple_stmt, [future_stmt, Newline()])
        for child in children:
            child.remove()
            new_node.append_child(child)
        tree.insert_child(0, new_node)
