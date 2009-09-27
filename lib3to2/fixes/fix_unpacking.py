"""
Fixer for:
(a,)* *b (,c)* [,] = s
for (a,)* *b (,c)* [,] in d: ...
"""

from lib2to3 import fixer_base
from lib2to3.pytree import Node, Leaf
from lib2to3.pygram import token, python_symbols as syms

class FixUnpacking(fixer_base.BaseFix):

    PATTERN = """
    expr_stmt< testlist_star_expr< pre=(any ',')* star_expr< '*' name=NAME > post=(',' any)* [','] > '=' target=any > |
    for_stmt< 'for' exprlist< pre=(any ',')* star_expr< '*' name=NAME > post=(',' any)* [','] > 'in' it=any ':' suite=any>"""

    def transform(self, node, results):
        """
        a,b,c,d,e,f,*g,h,i = range(100) changes to
        _3to2list=list(range(100));a,b,c,d,e,f,g,h,i = _3to2iter[:6] + [_3to2iter[6:-2]] + _3to2iter[-2:]

        and

        for a,b,*c,d,e in iter_of_iters: do_stuff changes to
        for _3to2iter in range(100):
            _3to2list = list(_3to2iter)
            a,b,c,d,e = _3to2list[:2] + [_3to2list[2:-2]] + _3to2list[-2:]
            do_stuff
        """
        # implementation goes here...
