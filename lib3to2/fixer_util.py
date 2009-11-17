from lib2to3.pygram import token, python_symbols as syms
from lib2to3.pytree import Leaf, Node
from lib2to3.fixer_util import Comma

def commatize(leafs):
    """
    Accepts/turns: (Name, Name, ..., Name, Name) 
    Returns/into: (Name, Comma, Name, Comma, ..., Name, Comma, Name)
    """
    new_leafs = []
    for leaf in leafs:
        new_leafs.append(leaf)
        new_leafs.append(Comma())
    del new_leafs[-1]
    return new_leafs

def indentation(node):
    """
    Recursively checks every previous sibling for token.INDENT

    Returns empty string if not found, or the indentation if it is.
    """
    prev_sibling = node.prev_sibling
    if node.type == token.INDENT:
        return node.value
    else:
        return indentation(prev_sibling) if prev_sibling is not None else ""

