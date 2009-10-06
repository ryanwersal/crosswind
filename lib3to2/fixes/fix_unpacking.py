"""
Fixer for:
(a,)* *b (,c)* [,] = s
for (a,)* *b (,c)* [,] in d: ...
"""

from lib2to3 import fixer_base
from lib2to3.pytree import Node, Leaf
from lib2to3.pygram import token, python_symbols as syms
from lib2to3.fixer_util import Assign, Call, Newline, Name, Number
from fix_imports2 import commatize

LISTNAME = u"_3to2list"
ITERNAME = u"_3to2iter"

def assignment_source(num_pre, num_post):
    """
    Accepts num_pre and num_post, which are counts of values
    before and after the starg (not including the starg)
    Returns a source fit for Assign() from fixer_util
    """
    # Ugly line... TODO: clean it up for readability
    source = Node(syms.arith_expr, [Node(syms.power, [Name(LISTNAME), Node(syms.trailer, [Leaf(token.LSQB, u"["), Node(syms.subscript, [Leaf(token.COLON, u":"), Number(num_pre)]), Leaf(token.RSQB, u"]")])]), Leaf(token.PLUS, u"+", prefix=u" "), Node(syms.power, [Leaf(token.LSQB, u"[", prefix=u" "), Name(LISTNAME), Node(syms.trailer, [Leaf(token.LSQB, u"["), Node(syms.subscript, [Number(num_pre), Leaf(token.COLON, u":"), Node(syms.factor, [Leaf(token.MINUS, u"-"), Number(num_post)])]), Leaf(token.RSQB, u"]"), Leaf(token.RSQB, u"]")])]), Leaf(token.PLUS, u"+", prefix=u" "), Node(syms.power, [Name(LISTNAME, prefix=u" "), Node(syms.trailer, [Leaf(token.LSQB, u"["), Node(syms.subscript, [Node(syms.factor, [Leaf(token.MINUS, u"-"), Number(num_post)]), Leaf(token.COLON, u":")]), Leaf(token.RSQB, u"]")])])])
    return source

class FixUnpacking(fixer_base.BaseFix):

    PATTERN = """
    expl=expr_stmt< testlist_star_expr<
        pre=(any ',')*
            star_expr< '*' name=NAME >
        post=(',' any)* [','] > '=' source=any > |
    impl=for_stmt< 'for' exprlist<
        pre=(any ',')*
            star_expr< '*' name=NAME >
        post=(',' any)* [','] > 'in' it=any ':' suite=any>"""

    def fix_explicit_context(self, node, results):
        pre, name, post, source = results.get("pre"), results.get("name"), results.get("post"), results.get("source")
        assert all((pre, name, post, source)), repr(node)
        pre = [n.clone() for n in pre if n.type == token.NAME]
        name.prefix = u" "
        post = [n.clone() for n in post if n.type == token.NAME]
        target = [n.clone() for n in commatize(pre + [name.clone()] + post)]
        source.prefix = u""
        setup_line = Assign(Name(LISTNAME), Call(Name(u"list"), [source.clone()]))
        power_line = Assign(target, assignment_source(len(pre), len(post)))
        return setup_line, power_line
        
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
        if expl is not None:
            setup_line, power_line = self.fix_explicit_context(node, results)
            setup_line.prefix = expl.prefix
            parent = node.parent
            i = node.remove()
            parent.insert_child(i, power_line)
            parent.insert_child(i, setup_line)
        else:
            self.fix_implicit_context(node, results) # do something with this
        
