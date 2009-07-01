"""Fixer for 'raise E(V).with_traceback(T)' -> 'raise E, V, T'"""

from lib2to3 import fixer_base
from lib2to3.pytree import Node, Leaf
from lib2to3.pgen2 import token
from lib2to3.fixer_util import Comma

class FixRaise(fixer_base.BaseFix):
    
    PATTERN = """
    raise_stmt< 'raise' power< exc=any trailer< '(' val=any* ')' >
        trailer< '.' 'with_traceback' > trailer< '(' trc=any ')' > > >"""
        
    def transform(self, node, results):
        syms = self.syms
        exc, val, trc = (results["exc"], results["val"], results["trc"])
        val = val[0] if val else Leaf(token.NAME, u"None")
        val.prefix = trc.prefix = u" "
        kids = [Leaf(token.NAME, u"raise"), exc.clone(), Comma(),
                val.clone(), Comma(), trc.clone()]
        raise_stmt = Node(syms.raise_stmt, kids)
        return raise_stmt
