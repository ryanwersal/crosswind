"""
Fixer for input(s) -> raw_input(s).
"""

from crosswind import fixer_base
from crosswind.fixer_util import Name


class FixInput(fixer_base.BaseFix):

    PATTERN = """
              power< name='input' trailer< '(' [any] ')' > any* >
              """

    def transform(self, node, results):
        name = results["name"]
        name.replace(Name("raw_input", prefix=name.prefix))
