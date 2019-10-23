"""
Fixer for "class Foo: ..." -> "class Foo(object): ..."
"""

from crosswind import fixer_base
from crosswind.fixer_util import Leaf, LParen, Name, Node, RParen, syms, token


def insert_object(node, idx):
    node.insert_child(idx, RParen())
    node.insert_child(idx, Name("object"))
    node.insert_child(idx, LParen())


class FixNewstyle(fixer_base.BaseFix):

    PATTERN = "classdef< 'class' NAME [paren='('] [')'] colon=':' any >"

    def transform(self, node, results):
        if "paren" in results:
            paren = results["paren"]
            idx = node.children.index(paren)
            node.insert_child(idx + 1, Name("object"))
        else:
            colon = results["colon"]
            idx = node.children.index(colon)
            insert_object(node, idx)
