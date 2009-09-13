"""
Fixer for print: from __future__ import print_function.
"Placeholder": In the future, this will transform print into a print statement
"""

from lib2to3 import fixer_base
from lib2to3.pytree import Node
from lib2to3.pygram import python_symbols as syms, token
from lib2to3.fixer_util import Name, FromImport, Newline

def gen_printargs(lst):
    """
    Accepts a list of all nodes in the print call's trailer.
    Returns a normalized list of argument nodes
    """
    for node in lst:
        if node.type == syms.arglist:
            # arglist < pos=any* kwargs=( argument < "file"|"sep"|"end" "=" any >* ) >
            kids = node.children
            it = kids.__iter__()
            try:
                while True:
                    arg = it.next()
                    if arg.type == syms.argument:
                        # argument < "file"|"sep"|"end" "=" (any) >
                        yield arg
                        # drop a comma, unless it is at the end
                        comma = it.next()
                        if comma.next_sibling is None:
                            yield comma
                    else:
                        yield arg
                        # drop a comma, unless it is at the end
                        comma = it.next()
                        if comma.next_sibling is None:
                            yield comma
            except StopIteration:
                continue
        else:
            yield node

def map_printargs(args):
    """
    Accepts a list of all nodes in the print call's trailer.
    Returns {'pos':[all,pos,args], 'sep':sep, 'end':end, 'file':file}
    May include {'trailing_comma':comma_node} in the mapping if there is a trailing comma.
    """
    printargs = [arg for arg in gen_printargs(args)]
#    for arg in printargs:
#        print repr(arg)

class FixPrint(fixer_base.BaseFix):

    def start_tree(self, tree, filename):
        """This is only run once; we want to remember the first node"""
        super(FixPrint, self).start_tree(tree, filename)
        self._tree = tree
        self.have_print = False

    PATTERN = """
              power< 'print' trailer < '(' args=any* ')' > any* >
              """

    def match(self, node):
        """
        Since the tree needs to be fixed once and only once if and only if it
        matches, then we can start discarding matches after we make the first.
        """
        return not self.have_print and super(FixPrint,self).match(node)

    def transform(self, node, results):
        tree = self._tree
        self.have_print = True
        args = results.get("args")
#        if args is not None:
#            map_printargs(args)
        future_stmt = FromImport(u"__future__",
                                [Name(u"print_function", prefix=u" ")])
        children = tree.children[:]
        new_node = Node(syms.simple_stmt, [future_stmt, Newline()])
        for child in children:
            child.remove()
            new_node.append_child(child)
        tree.insert_child(0, new_node)
