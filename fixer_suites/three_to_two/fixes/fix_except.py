"""
Fixer for except E as T -> except E, T
"""

from crosswind import fixer_base
from crosswind.fixer_util import Comma


class FixExcept(fixer_base.BaseFix):

    PATTERN = """except_clause< 'except' any as='as' any >"""

    def transform(self, node, results):
        results["as"].replace(Comma())
