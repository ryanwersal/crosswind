"""
Fixer for f.__x__ -> f.func_x.
"""

from crosswind import fixer_base
from crosswind.fixer_util import Name


class FixFuncattrs(fixer_base.BaseFix):

    PATTERN = """
    power< any+ trailer< '.' attr=('__closure__' | '__globals__' |
                                   '__defaults__' | '__code__' ) > any* >
    """

    def transform(self, node, results):
        attr = results["attr"][0]
        attr.replace(Name(("func_%s" % attr.value.strip("_")), prefix=attr.prefix))
