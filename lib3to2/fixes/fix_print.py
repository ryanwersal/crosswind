"""
Fixer for print.
Currently, this can be seen as a "placeholder":  All it does is add a
future_stmt to the top that includes the print_function, so the resulting code
is only compatible with 2.6+.
"""

from lib2to3 import fixer_base, pytree
from lib2to3.fixer_util import (Name, Comma, FromImport, touch_import, Newline,
                                is_probably_builtin)
from lib2to3.pgen2 import token
from lib2to3.pygram import python_symbols as syms

class FixPrint(fixer_base.BaseFix):

    PATTERN = """
              power< 'print' trailer < '(' any* ')' > any* >
              """
              
    def transform(self, node, results):
        _node = node
        if not is_probably_builtin(node):
            return
        while _node.parent is not None:
            _node = _node.parent
        future_stmt = FromImport(u'__future__',
                                 [pytree.Leaf(token.NAME, u'print_function',
                                 prefix=u' ')])
        children = list(_node.children[:])
        for child in children:
            child.remove()
        children = [future_stmt, Newline()] + children
        newnode = pytree.Node(syms.simple_stmt, children)
        _node.insert_child(0, newnode)
