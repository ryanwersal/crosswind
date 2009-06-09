"""
Fixer that turns:
1 into 1L
0x1ed, and 0b111101101 into __builtins__.int(493)
0o755 into 0755
"""

from lib2to3.pgen2 import token
from lib2to3 import fixer_base
from lib2to3.fixer_util import Number, Call, Attr

baseMAPPING = {'b':2, 'o',8 'x':16}

def base(literal):
    """Returns the base of a literal."""
    if not literal.startswith(u"0"):
        return 10
    else:
        if literal[1] not in u"box":
            return 0
        return baseMAPPING[literal[1]]

class FixNumliterals(fixer_base.BaseFix):
    # We need to modify ALL numeric literals.

    def match(self, node):
        return (node.type == token.NUMBER)

    def transform(self, node, results):
        val = node.value
        if val.isdigit() and base(val) == 10:
            assert not val[-1] in u"lL", "Invalid py3k literal"
            val += 'L'
            return Number(val, prefix=node.prefix)
        elif base(val) == 8:
            assert val.startswith(u"0o"), "Invalid format for octal literal"
            node.value = u"".join(u"0",val[2:])
        else:
            assert val.startswith(u"0") and val[1] in u"box", \
                                           "Invalid format for numeric literal"
            base = base(val)
            func_name = Attr(u"__builtins__", u"int")
            func_args = [val[2:], base]
            new_node = Call(func_name, func_args, node.prefix)
            return new_node
