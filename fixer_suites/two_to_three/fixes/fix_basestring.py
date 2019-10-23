"""Fixer for basestring -> str."""
# Author: Christian Heimes

# Local imports
from crosswind import fixer_base
from crosswind.fixer_util import Call, Comma, Name, ArgList


class FixBasestring(fixer_base.BaseFix):
    BM_compatible = True

    PATTERN = "power< 'isinstance' trailer< '(' args=arglist< any ',' basestring='basestring' > ')' > >"

    def transform(self, node, results):
        args = results["args"]
        args.children[-1].replace(Name("str", prefix=results["basestring"].prefix))
        args = [a.clone() for a in args.children]
        return Call(Name("isinstance"), args=args, prefix=node.prefix)
