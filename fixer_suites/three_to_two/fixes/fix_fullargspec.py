"""
Fixer for getfullargspec -> getargspec
"""

from crosswind import fixer_base
from crosswind.fixer_util import Name


warn_msg = "some of the values returned by getfullargspec are not valid in Python 2 and have no equivalent."


class FixFullargspec(fixer_base.BaseFix):

    PATTERN = "'getfullargspec'"

    def transform(self, node, results):
        self.warning(node, warn_msg)
        return Name("getargspec", prefix=node.prefix)
