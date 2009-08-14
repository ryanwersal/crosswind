"""
Fixer for:
0b111101101 -> __builtins__.long("111101101", 2)
0o755 -> 0755
"""

import re

from lib2to3.pgen2 import token
from lib2to3 import fixer_base
from lib2to3.pygram import python_symbols as syms
from lib2to3.pytree import Node
from lib2to3.fixer_util import Number, Call, Attr, String, Name, ArgList, Comma

baseMAPPING = {'b':2, 'o':8, 'x':16}

class FixNumliterals(fixer_base.BaseFix):
    # We need to modify all numeric literals except floats, complex.

    def base(self, literal):
        """Returns the base of a valid py3k literal."""
        literal = literal.strip()
        #All literals that do not start with 0, or are 1 or more zeros.
        if not literal.startswith(u"0") or re.match(r"0+$",literal):
            return 10
        elif literal[1] not in u"box":
            return 0
        return baseMAPPING[literal[1]]

    def unmatch(self, node):
        """Don't match complex numbers, floats, or base-10 ints"""
        val = node.value
        for bad in u"jJ+-.":
            if bad in val: return bad
        base = self.base(val)
        return base == 10 or base == 16

    def match(self, node):
        return (node.type == token.NUMBER) and not self.unmatch(node)

    def transform(self, node, results):
        """
        Call __builtins__.long() with the value and the base of the value.
        This works because 0b10 is int("10", 2), 0o10 is int("10", 8), etc.
        """
        val = node.value
        base = self.base(val)
        if base == 8:
            assert val.strip().startswith(u"0o") or \
            val.strip().startswith(u"0O"), "Invalid format for octal literal"
            node.changed()
            node.value = u"".join((u"0",val[2:]))
        elif base == 2:
            assert val.startswith(u"0") and val[1] in u"bB", \
                                           "Invalid format for binary literal"
            # __builtins__.long
            func_name = Node(syms.power, Attr(Name(u"__builtins__"), \
                             Name(u"long")))
            # ("...", 2)
            func_args = [String(u"".join((u"\"", val.strip()[2:], u"\""))), \
                         Comma(), Number(2, prefix=u" ")]
            new_node = Call(func_name, func_args, node.prefix)
            return new_node
