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

    PATTERN = u"classdef< 'class' NAME [paren='('] [')'] colon=':' any >"

    def transform(self, node, results):
        if 'paren' in results:
            paren = results[u'paren']
            idx = node.children.index(paren)
            node.insert_child(idx + 1, Name(u"object"))
        else:
            colon = results[u'colon']
            idx = node.children.index(colon)
            insert_object(node, idx)
        