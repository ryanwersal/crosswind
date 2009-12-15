"""
Fixer for:
(a,)* *b (,c)* [,] = s
for (a,)* *b (,c)* [,] in d: ...
"""

from lib2to3 import fixer_base
from lib2to3.pytree import Node, Leaf
from lib2to3.pygram import token, python_symbols as syms
from lib2to3.fixer_util import Assign, Comma, Call, Newline, Name, Number

from ..fixer_util import indentation
from fix_imports2 import commatize

def assignment_source(num_pre, num_post, LISTNAME, ITERNAME):
    """
    Accepts num_pre and num_post, which are counts of values
    before and after the starg (not including the starg)
    Returns a source fit for Assign() from fixer_util
    """
    children = []
    pre = str(num_pre)
    post = str(num_post)
    # a little prettier... still some cleanup TODO
    if num_pre > 0:
        pre_part = Node(syms.power, [Name(LISTNAME), Node(syms.trailer, [Leaf(token.LSQB, u"["), Node(syms.subscript, [Leaf(token.COLON, u":"), Number(pre)]), Leaf(token.RSQB, u"]")])])
        children.append(pre_part)
        children.append(Leaf(token.PLUS, u"+", prefix=u" "))
    main_part = Node(syms.power, [Leaf(token.LSQB, u"[", prefix=u" "), Name(LISTNAME), Node(syms.trailer, [Leaf(token.LSQB, u"["), Node(syms.subscript, [Number(pre) if num_pre > 0 else Leaf(1, u""), Leaf(token.COLON, u":"), Node(syms.factor, [Leaf(token.MINUS, u"-"), Number(post)]) if num_post > 0 else Leaf(1, u"")]), Leaf(token.RSQB, u"]"), Leaf(token.RSQB, u"]")])])
    children.append(main_part)
    if num_post > 0:
        children.append(Leaf(token.PLUS, u"+", prefix=u" "))
        post_part = Node(syms.power, [Name(LISTNAME, prefix=u" "), Node(syms.trailer, [Leaf(token.LSQB, u"["), Node(syms.subscript, [Node(syms.factor, [Leaf(token.MINUS, u"-"), Number(post)]), Leaf(token.COLON, u":")]), Leaf(token.RSQB, u"]")])])
        children.append(post_part)
    source = Node(syms.arith_expr, children)
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
        pre = [n.clone() for n in pre if n.type == token.NAME]
        name.prefix = u" "
        post = [n.clone() for n in post if n.type == token.NAME]
        target = [n.clone() for n in commatize(pre + [name.clone()] + post)]
        # to make the special-case fix for "*z, = ..." correct with the least
        # amount of modification, make the left-side into a guaranteed tuple
        target.append(Comma())
        source.prefix = u""
        setup_line = Assign(Name(self.LISTNAME), Call(Name(u"list"), [source.clone()]))
        power_line = Assign(target, assignment_source(len(pre), len(post), self.LISTNAME, self.ITERNAME))
        return setup_line, power_line
        
    def fix_implicit_context(self, node, results):
        """
        Only example of the implicit context is
        a for loop, so only fix that.
        """
        self.cannot_convert(node, "Not implemented yet.")


    def transform(self, node, results):
        """
        a,b,c,d,e,f,*g,h,i = range(100) changes to
        _3to2list = list(range(100))
        a,b,c,d,e,f,g,h,i = _3to2iter[:6] + [_3to2iter[6:-2]] + _3to2iter[-2:]

        and

        for a,b,*c,d,e in iter_of_iters: do_stuff changes to
        for _3to2iter in iter_of_iters:
            _3to2list = list(_3to2iter)
            a,b,c,d,e = _3to2list[:2] + [_3to2list[2:-2]] + _3to2list[-2:]
            do_stuff
        """
        self.LISTNAME = self.new_name("_3to2list")
        self.ITERNAME = self.new_name("_3to2iter")
        expl, impl = results.get("expl"), results.get("impl")
        if expl is not None:
            setup_line, power_line = self.fix_explicit_context(node, results)
            setup_line.prefix = expl.prefix
            power_line.prefix = indentation(expl.parent)
            setup_line.append_child(Newline())
            parent = node.parent
            i = node.remove()
            parent.insert_child(i, power_line)
            parent.insert_child(i, setup_line)
        elif impl is not None:
            self.fix_implicit_context(node, results) # do something with this
