"""
Fixer for:
functools.reduce(f, it) -> reduce(f, it)
from functools import reduce -> (remove this line)
"""

from lib2to3 import fixer_base
from lib2to3.fixer_util import Call
from lib2to3.pytree import Node, Leaf
from lib2to3.pgen2 import token

class FixReduce(fixer_base.BaseFix):

    PATTERN = """
    power< 'functools' trailer< '.' 'reduce' >
                                    args=trailer< '(' arglist< any* > ')' > > |
    imported=import_from< 'from' 'functools' 'import' 'reduce' > |
    import_from< 'from' 'functools' 'import' import_as_names< any* in_list='reduce' any* > >
    """

    def transform(self, node, results):
        syms = self.syms
        args, imported = (results.get("args"), results.get("imported"))
        in_list = results.get("in_list")
        if imported:
            next = imported.next_sibling
            if next.type == token.NEWLINE:
                next.remove()
            imported.remove()
        elif args:
            args = args.clone()
            prefix = node.prefix
            return Node(syms.power, [Leaf(token.NAME, "reduce"), args],
                                                                 prefix=prefix)
        elif in_list:
            next = in_list.next_sibling
            if next is not None:
                if next.type == token.COMMA:
                    next.remove()
            else:
                prev = in_list.prev_sibling
                if prev is not None:
                    if prev.type == token.COMMA:
                        prev.remove()
            in_list.remove()
