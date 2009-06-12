"""
Fixer for print: from __future__ import print_function.
"Placeholder": In the future, this will transform print into a print statement
"""

from lib2to3 import fixer_base, pytree
from lib2to3.fixer_util import (Name, Comma, FromImport, touch_import, Newline,
                                is_probably_builtin)
from lib2to3.pgen2 import token

class FixPrint(fixer_base.BaseFix):

    PATTERN = """
              power< 'print' trailer < '(' any* ')' > any* >
              """
              
    def transform(self, node, results):
        _node = node
        if not is_probably_builtin(node):
            return
        syms = self.syms
        while _node.parent is not None:
            _node = _node.parent
        # If we've already added a future_stmt before... don't add another!
        if '_node' in dir(self.__class__) and _node is self.__class__._node:
            return
        future_stmt = FromImport(u'__future__',
                                 [pytree.Leaf(token.NAME, u'print_function',
                                 prefix=u' ')])
        children = list(_node.children[:])
        for child in children:
            child.remove()
        children = [future_stmt, Newline()] + children
        newnode = pytree.Node(syms.simple_stmt, children)
        _node.insert_child(0, newnode)
        #Save our last fix... we don't want to add multiple future_stmts
        self.__class__._node = _node
