"""Fixer that changes input(...) into raw_input(...)."""
# Author: Joe Amenta

# This fixer is a copy-paste of lib2to3/fixes/fix_raw_input.py by Andre Roberge,
# with input and raw_input switched.

# Local imports
from lib2to3 import fixer_base
from lib2to3.fixer_util import Name

class FixInput(fixer_base.BaseFix):

    PATTERN = """
              power< name='input' trailer< '(' [any] ')' > any* >
              """

    def transform(self, node, results):
        name = results["name"]
        name.replace(Name("raw_input", prefix=name.get_prefix()))
