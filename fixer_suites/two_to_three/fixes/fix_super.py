"""
Fixer for:

def something(self):
    super(self.__class__, self)

->

def something(self):
    super()
"""

from crosswind import fixer_base
from crosswind.fixer_util import Name


class FixSuper(fixer_base.BaseFix):

    PATTERN = "power< 'super' trailer< '(' func_args=arglist< any* > ')' > any* >"

    def transform(self, node, results):
        func_args = results["func_args"]
        func_args.replace(Name("", prefix=func_args.prefix))
