"""Fixer for basestring -> str."""
# Author: Christian Heimes

# Local imports
from crosswind import fixer_base
from crosswind.fixer_util import Name, _find


class FixBasestring(fixer_base.BaseFix):
    BM_compatible = True

    PATTERN = """
        power< 'isinstance' trailer< '(' args=arglist< any* > ')' > >
    """

    def transform(self, node, results):
        basestring_node = _find("basestring", results["args"])
        if basestring_node is None:
            return

        basestring_node.replace(Name("str", prefix=basestring_node.prefix))
