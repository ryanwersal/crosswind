"""
Fixer that changes zip(...) into list(zip(...)),
unless the list functionality is not needed.
"""

# Local imports
from lib2to3 import fixer_base
from lib2to3.fixer_util import Name, Call, in_special_context


class FixZip(fixer_base.BaseFix):

    PATTERN = """
              power< 'zip' args=trailer< '(' [any] ')' > >
              """

    def transform(self, node, results):
        if in_special_context(node):
            return

        new = node.clone()
        new.set_prefix(u"")
        return Call(Name(u"list"), [new], prefix=node.get_prefix())
