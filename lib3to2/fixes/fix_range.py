"""
Fixer for range(s) -> xrange(s).
"""

from lib2to3 import fixer_base
from lib2to3.fixer_util import Name

class FixRange(fixer_base.BaseFix):

    PATTERN = """
              power<
                 (name='range') trailer< '(' args=any ')' >
              rest=any* >
              """

    def transform(self, node, results):
        name = results['name']
        name.replace(Name(u'xrange', prefix=name.prefix))
