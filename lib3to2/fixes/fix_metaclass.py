"""
Fixer for (metaclass=X) -> __metaclass__ = X
Some semantics (see PEP 3115) may be altered in the translation."""

from lib2to3 import fixer_base
from lib2to3.fixer_util import Name, syms, Node, Leaf
from lib2to3.pygram import token

class FixMetaclass(fixer_base.BaseFix):

    PATTERN = """
    classdef<any*>
    """
    
    def transform(self, node, results):
        meta = self.has_metaclass(node)
        if not meta: return
        meta.remove()
        target = Leaf(token.NAME, u"__metaclass__")
        equal = Leaf(token.EQUAL, u"=", prefix=u" ")
        meta.prefix = u" "
        stmt_node = Node(syms.atom, [target, equal, meta])
        
    def has_metaclass(self, parent):
        name = None
        for node in parent.children:
            kids = node.children
            if node.type == syms.argument:
                if kids[0] == Leaf(token.NAME, u"metaclass") and \
                   kids[1] == Leaf(token.EQUAL, u"=") and \
                   kids[2]:
                #One argument, it's the (metaclass=X) part...
                    name = kids[2]
            elif node.type == syms.arglist:
                #Argument list... loop through it looking for:
                #Node(*, [*, Leaf(token.NAME, u"metaclass"), Leaf(token.EQUAL, u"="), Leaf(*, *)]
                for child in node.children:
                    if type(child) == Node:
                        meta = equal = None
                        for arg in child.children:
                            if arg == Leaf(token.NAME, u"metaclass"):
                                #We have the (metaclass) part
                                meta = arg
                            elif meta and arg == Leaf(token.EQUAL, u"="):
                                #We have the (metaclass=) part
                                equal = arg
                            elif meta and equal:
                                #Here we go, we have (metaclass=X)
                                name = arg
                            elif name:
                                raise SyntaxError("Argument after metaclass=X")
        return name
