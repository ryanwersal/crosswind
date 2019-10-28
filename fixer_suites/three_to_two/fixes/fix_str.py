"""
Fixer for:
str -> unicode
chr -> unichr
"spam" -> u"spam"
"""

import re

from crosswind import fixer_base
from crosswind.fixer_util import Name
from crosswind.pgen2 import token


_literal_re = re.compile(r"[rR]?[\'\"]")


class FixStr(fixer_base.BaseFix):

    order = "pre"
    run_order = 4  # Run this before bytes objects are converted to str objects

    PATTERN = "STRING | 'str'"

    def transform(self, node, results):
        new = node.clone()
        if node.type == token.STRING:
            # Simply add u to the beginning of the literal.
            if _literal_re.match(new.value):
                new.value = "u" + new.value
                return new
        elif node.type == token.NAME and new.value == "str":
            new.value = "unicode"
            return new
