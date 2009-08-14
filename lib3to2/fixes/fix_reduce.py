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
    imported=import_from< 'from' 'functools' 'import' 'reduce' >
    """

    def transform(self, node, results):
        syms = self.syms
        args, imported = (results.get("args"), results.get("imported"))
        if imported:
            imported.remove()
        elif args:
            args = args.clone()
            prefix = node.prefix
            return Node(syms.power, [Leaf(token.NAME, u"reduce"), args],
                                                                 prefix=prefix)
