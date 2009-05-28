"""Fixer that changes range(...) into xrange(...)."""

# Local imports
from lib2to3 import fixer_base
from lib2to3.fixer_util import Name, Call, consuming_calls
from lib2to3 import patcomp


class FixRange(fixer_base.BaseFix):

    PATTERN = """
              power<
                 (name='range') trailer< '(' args=any ')' >
              rest=any* >
              """

    def transform(self, node, results):
        name = results['name']
        name.replace(Name(u'xrange', prefix=name.get_prefix()))
