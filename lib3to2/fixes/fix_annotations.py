"""
Fixer to remove function annotations
"""

from lib2to3 import fixer_base
from lib2to3.pgen2 import token
from lib2to3.fixer_util import syms

def param_without_annotations(node):
    return node.children[0]

class FixAnnotations(fixer_base.BaseFix):

    PATTERN = """
              funcdef< 'def' any parameters< '(' [params=any] ')' > ['->' ret=any] ':' any* >
              """

    def transform(self, node, results):
        """
        This just strips annotations from the funcdef completely.
        """
        params = results.get("params")
        ret = results.get("ret")
        if ret is not None:
            assert ret.prev_sibling.type == token.RARROW, "Invalid return annotation"
            ret.prev_sibling.remove()
            ret.remove()
        if params is None: return
        if params.type == syms.typedargslist:
            # more than one param in a typedargslist
            for param in params.children:
                if param.type == syms.tname:
                    param.replace(param_without_annotations(param))
        elif params.type == syms.tname:
            # one param
            params.replace(param_without_annotations(params))
