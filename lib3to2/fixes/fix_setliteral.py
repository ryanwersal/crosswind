"""Fixer for '{1, 2, 3}' -> 'set([1, 2, 3])'"""

from lib2to3 import fixer_base
from lib2to3.pytree import Node, Leaf
from lib2to3.pgen2 import token
from lib2to3.fixer_util import Name, LParen, RParen

def unmatch_dict(node):
    """Placeholder for now"""
    pass

class FixSetliteral(fixer_base.BaseFix):
    
    PATTERN = """atom< '{' dictsetmaker< args=any* > '}' > |
                 atom< '{' arg=any '}' >"""
    
    explicit = True # only because it grabs dicts too right now.
    
    def transform(self, node, results):
        syms = self.syms
        prefix = node.prefix
        args = results.get("args")
        arg = results.get("arg")
        if args:
            for i, arg in enumerate(args):
                args[i] = arg.clone()
            args = Node(syms.atom, [Leaf(token.LSQB, u"["),
                                    Node(syms.listmaker, args),
                                    Leaf(token.RSQB, u"]")])
        elif arg:
            arg = arg.clone()
            arg = Node(syms.atom, [Leaf(token.LSQB, u"["),
                                   Node(syms.listmaker, [arg]),
                                   Leaf(token.RSQB, u"]")])
        return Node(syms.power, [Name(u"set"), LParen(), args or arg, RParen()], 
                                                                 prefix=prefix)
