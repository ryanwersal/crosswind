"""
Fixer for:

def something(self):
    super()

->

def something(self):
    super(self.__class__, self)
"""

from lib2to3 import fixer_base
from ..fixer_util import Node, Leaf, token, syms, Name, Comma, Dot

dot_class = Node(syms.trailer, [Dot(), Name("__class__")])

def get_firstparam(super_node):
    parent = super_node.parent
    while parent.type != syms.funcdef and parent.parent:
        parent = parent.parent

    if parent.type != syms.funcdef:
        return None

    children = parent.children
    assert len(children) > 2
    params = children[2]
    assert params.type == syms.parameters and len(params.children) > 2
    name = params.children[1]
    assert name.type == token.NAME
    return name.value

def insert_args(name, rparen):
    parent = rparen.parent
    idx = parent.children.index(rparen)
    parent.insert_child(idx, Name(name, prefix=" "))
    parent.insert_child(idx, Comma())
    parent.insert_child(idx, Node(syms.power, [Name(name), dot_class.clone()]))


class FixSuper(fixer_base.BaseFix):

    PATTERN = "power< 'super' trailer< '(' rparen=')' > any* >"

    def transform(self, node, results):
        param = get_firstparam(node)
        rparen = results["rparen"]
        insert_args(param, rparen)
