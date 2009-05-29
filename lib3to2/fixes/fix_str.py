"""Fixer that changes str to unicode, chr to unichr, and "..." into u"...".

"""

import re
from lib2to3.pgen2 import token
from lib2to3 import fixer_base
from lib2to3.fixer_util import Name

_mapping = {u"chr":u"unichr", u"str":u"unicode"}
_literal_re = re.compile(ur"[rR]?[\'\"]")

class FixStr(fixer_base.BaseFix):

    PATTERN = "STRING | 'str' | 'chr'"

    def transform(self, node, results):
        new = node.clone()
        if node.type == token.STRING:
            if _literal_re.match(new.value):
                new.value = u"u" + new.value
                return new
        elif node.type == token.NAME:
            assert new.value in _mapping
            new.value = _mapping[new.value]
            return new
