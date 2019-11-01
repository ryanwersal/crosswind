"""
Fixer for getargspec -> getfullargspec
"""

from crosswind import fixer_base
from crosswind.fixer_util import Name


class FixArgspec(fixer_base.BaseFix):

    PATTERN = "'getargspec'"

    def transform(self, node, results):
        return Name("getfullargspec", prefix=node.prefix)
