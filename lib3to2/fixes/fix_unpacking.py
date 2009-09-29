"""
Fixer for:
(a,)* *b (,c)* [,] = s
for (a,)* *b (,c)* [,] in d: ...
"""

from lib2to3 import fixer_base
from lib2to3.pytree import Node, Leaf
from lib2to3.pygram import token, python_symbols as syms

LISTNAME = u"_3to2list"
ITERNAME = u"_3to2iter"

def assignment_stmt(pre, starg, post):
    """
    Accepts a list of mandatory argument names before the star_expr,
    the star_expr name itself,
    and a list of mandatory argument names after the star_expr
    Returns a node of the form"
    pre, starg, post = _3to2iter[:len(pre)] + \
                      [_3to2iter[len(pre):-len(post)]] + \
                       _3to2iter[-len(post):]
    """
    pass

class FixUnpacking(fixer_base.BaseFix):

    PATTERN = """
    expl=expr_stmt< testlist_star_expr<
        pre=(any ',')*
            star_expr< '*' name=NAME >
        post=(',' any)* [','] > '=' from=any > |
    impl=for_stmt< 'for' exprlist<
        pre=(any ',')*
            star_expr< '*' name=NAME >
        post=(',' any)* [','] > 'in' it=any ':' suite=any>"""

    def fix_explicit_context(self, node, results):
        pass

    def fix_implicit_context(self, node, results):
        pass

    def transform(self, node, results):
        """
        a,b,c,d,e,f,*g,h,i = range(100) changes to
        _3to2list=list(range(100))
        a,b,c,d,e,f,g,h,i = _3to2iter[:6] + [_3to2iter[6:-2]] + _3to2iter[-2:]

        and

        for a,b,*c,d,e in iter_of_iters: do_stuff changes to
        for _3to2iter in range(100):
            _3to2list = list(_3to2iter)
            a,b,c,d,e = _3to2list[:2] + [_3to2list[2:-2]] + _3to2list[-2:]
            do_stuff
        """
        expl, impl = results.get("expl"), results.get("impl")
        return self.fix_implicit_context(node, results) if impl is not None \
          else self.fix_explicit_context(node, results)
