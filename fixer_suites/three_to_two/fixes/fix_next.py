"""
Fixer for:
it.__next__() -> it.next().
next(it) -> it.next().
"""

from crosswind import fixer_base
from crosswind.fixer_util import Attr, Call, Name, find_binding
from crosswind.pgen2 import token
from crosswind.pygram import python_symbols as syms


bind_warning = "Calls to builtin next() possibly shadowed by global binding"


class FixNext(fixer_base.BaseFix):

    PATTERN = """
    power< base=any+ trailer< '.' attr='__next__' > any* >
    |
    power< head='next' trailer< '(' arg=any ')' > any* >
    |
    classdef< 'class' base=any+ ':'
              suite< any*
                     funcdef< 'def'
                              attr='__next__'
                              parameters< '(' NAME ')' > any+ >
                     any* > >
    """

    def transform(self, node, results):
        assert results

        base = results.get("base")
        attr = results.get("attr")
        head = results.get("head")
        arg_ = results.get("arg")
        if arg_:
            arg = arg_.clone()
            head.replace(Attr(Name(str(arg), prefix=head.prefix), Name("next")))
            arg_.remove()
        elif base:
            attr.replace(Name("next", prefix=attr.prefix))
