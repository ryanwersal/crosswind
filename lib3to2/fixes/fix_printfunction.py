"""
Fixer for print: from __future__ import print_function.
"""

from lib2to3 import fixer_base
from lib2to3.pytree import Node
from lib2to3.pygram import python_symbols as syms
from lib2to3.fixer_util import Name, FromImport, Newline

class FixPrintfunction(fixer_base.BaseFix):

    explicit = True # Not the preferred way to fix print

    def start_tree(self, tree, filename):
        """This is only run once; we want to remember the first node"""
        super(FixPrintfunction, self).start_tree(tree, filename)
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
        return not self.have_print and super(FixPrintfunction,self).match(node)

    def transform(self, node, results):
        tree = self._tree
        self.have_print = True
        future_stmt = FromImport(u"__future__",
                                [Name(u"print_function", prefix=u" ")])
        children = tree.children[:]
        new_node = Node(syms.simple_stmt, [future_stmt, Newline()])
        for child in children:
            child.remove()
            new_node.append_child(child)
        tree.insert_child(0, new_node)
