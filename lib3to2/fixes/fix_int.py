"""
Fixer for:
int -> long
123 -> 123L
"""

from lib2to3 import fixer_base
from lib2to3.fixer_util import Name, is_probably_builtin, Number
from lib2to3.pgen2 import token

baseMAPPING = {'b':2, 'o':8, 'x':16}

class FixInt(fixer_base.BaseFix):
    
    explicit = True # In most cases, 3.x ints will work just like 2.x ints.
    
    PATTERN = "'int' | NUMBER"

    static_long = Name(u"long")
    
    def base(self, literal):
        """Returns the base of a valid py3k numeric literal."""
        literal = literal.strip()
        if not literal.startswith(u"0"):
            return 10
        else:
            if literal[1] not in u"box":
                return 0
            return baseMAPPING[literal[1]]
            
    def unmatch(self, node):
        """Don't match complex numbers, floats, or longs"""
        val = node.value
        #For whatever reason, some ints are being matched after we fix them.
        if val.endswith("L"):
            return "L"
        for bad in u"jJ+-.":
            if bad in val: return bad
            
    def match(self, node):
        return super(FixInt, self).match(node) and not self.unmatch(node)

    def transform(self, node, results):
        val = node.value
        if node.type == token.NUMBER and self.base(val) == 10:
            assert not val[-1] in u"lL", "Invalid py3k literal: " + str(val)
            val += u"L"
            return Number(val, prefix=node.prefix)
        elif is_probably_builtin(node):
            assert node.type == token.NAME, "Sanity check failed: " + str(val)
            new = self.static_long.clone()
            new.prefix = node.prefix
            return new
