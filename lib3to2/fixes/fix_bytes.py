"""Fixer that changes bytes to str.

"""

import re
from lib2to3.pgen2 import token
from lib2to3 import fixer_base
from lib2to3.fixer_util import Name

_literal_re = re.compile(ur"[bB][rR]?[\'\"]")

class FixBytes(fixer_base.BaseFix):
    
    PATTERN = "STRING | 'bytes'"

    def transform(self, node, results):
        new = node.clone()
        if node.type == token.NAME:
            assert new.value == u'bytes'
            new.value = u"str"
            return new
        elif node.type == token.STRING:
            if _literal_re.match(node.value):
                new.value = new.value[1:]
                return new

