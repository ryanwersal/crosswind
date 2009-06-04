"""
Fixer for print.
Currently, this can be seen as a "placeholder":  All it does is add a
future_stmt to the top that includes the print_function, so the resulting code
is only compatible with 2.6+.
"""

from lib2to3 import fixer_base, pytree
from lib2to3.fixer_util import Name, Comma, FromImport
from lib2to3.pgen2 import token

class FixPrint(fixer_base.BaseFix):

    PATTERN = """
              'print'
              """

    def transform(self, node, results):
        _node = node
        while _node.parent is not None:
            _node = _node.parent
        future_stmt = FromImport(u'__future__',
                                 [pytree.Leaf(token.NAME, u'print_function',
                                 prefix=u' ')])
        _node.parent = future_stmt
        #XXX Right here, the future_stmt needs to (somehow) turn into the 
        #XXX first node of the tree.
