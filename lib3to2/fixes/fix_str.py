"""Fixer that changes str to unicode, chr to unichr, and "..." into u"...".

"""

import re
from lib2to3.pgen2 import token
from lib2to3 import fixer_base

class FixStr(fixer_base.BaseFix):

    PATTERN = "STRING | NAME<'str' | 'chr'>"

    def transform(self, node, results):
        if node.type == token.NAME:
            if node.value == u"str":
                new = node.clone()
                new.value = u"unicode"
                return new
            if node.value == u"chr":
                new = node.clone()
                new.value = u"unichr"
                return new
        elif node.type == token.STRING:
            if re.match(ur"[rR]?[\'\"]", node.value):
                new = node.clone()
                new.value = u"u" + new.value
                return new
