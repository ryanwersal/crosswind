"""
Fixer to remove function annotations
"""

from lib2to3 import fixer_base
from lib2to3.pgen2 import token
from lib2to3.fixer_util import syms

def param_without_annotations(node):
    return node.children[0] if node.type == syms.tname else node

class FixAnnotations(fixer_base.BaseFix):

    PATTERN = """
              funcdef< 'def' any parameters< '(' params=any* ')' > ['->' ret=any] ':' any* >
              """

    def transform(self, node, results):
        """
        This just strips annotations from the funcdef completely.
        """
        params = results["params"]
        ret = results.get("ret")
        if ret is not None:
            assert ret.prev_sibling.type == token.RARROW, "Invalid return annotation"
            ret.prev_sibling.remove()
            ret.remove()
        for param_node in params:
            if param_node.type == syms.typedargslist:
                # more than one param in a typedargslist
                for param in param_node.children:
                    param.replace(param_without_annotations(param))
            elif param_node.type == syms.tname:
                # one param
                param_node.replace(param_without_annotations(param_node))
