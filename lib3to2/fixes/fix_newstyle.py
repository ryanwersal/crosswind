"""
Fixer for "class Foo: ..." -> "class Foo(object): ..."
"""

from lib2to3 import fixer_base
from ..fixer_util import Node, Leaf, token, syms, LParen, RParen, Name

def insert_object(node, idx):
    node.insert_child(idx, RParen())
    node.insert_child(idx, Name("object"))
    node.insert_child(idx, LParen())

class FixNewstyle(fixer_base.BaseFix):

    PATTERN = "classdef< 'class' NAME colon=':' any >"

    def transform(self, node, results):
        colon = results["colon"]
        idx = node.children.index(colon)
        insert_object(node, idx)
