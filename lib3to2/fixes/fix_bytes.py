"""Fixer that changes bytes to str.

"""

import re
from lib2to3.pgen2 import token
from lib2to3 import fixer_base

class FixBytes(fixer_base.BaseFix):
    
    PATTERN = """STRING | NAME< 'bytes' >"""

    def transform(self, node, results):
        if node.type == token.NAME:
            if node.value == u"bytes":
                new = node.clone()
                new.value = u"str"
                return new
        elif node.type == token.STRING:
            if re.match(ur"[bB][rR]?[\'\"]", node.value):
                new = node.clone()
                new.value = unicode(new.value[1:])
                return new
