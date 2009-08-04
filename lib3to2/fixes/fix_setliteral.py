"""Fixer for '{1, 2, 3}' -> 'set([1, 2, 3])'"""

from lib2to3 import fixer_base
from lib2to3.pytree import Node, Leaf
from lib2to3.pgen2 import token
from lib2to3.fixer_util import Name, LParen, RParen

def found_dict(node):
    """The pattern will match dicts, too, so we need to change that."""
    try:
        return type(eval(str(node))) == dict 
    except SyntaxError:
        #All set literals will raise syntax errors when eval()ed in 2.x
        from sys import version_info
        assert version_info[0] == 2, u"fix_setliteral fails to account for dicts when run in Python versions higher than 2.x"
        return False

class FixSetliteral(fixer_base.BaseFix):
    
    PATTERN = """atom< '{' dictsetmaker< args=any* > '}' > |
                 atom< '{' arg=any '}' >"""
    
    def match(self, node):
        results = super(FixSetliteral, self).match(node)
        if results and not found_dict(node):
            return results
        else:
            return False
    
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
