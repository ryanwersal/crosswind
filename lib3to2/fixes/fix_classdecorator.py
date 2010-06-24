"""
Fixer to remove class decorators
"""

from lib2to3 import fixer_base
from lib2to3.fixer_util import Call, Assign, String, Newline
from ..fixer_util import Leaf, Node, token, syms, indentation

def call_chain(inner_name, names):
    """
    Accepts an inner name and a sequence
    Returns a chain of calls by that sequence on the inner name.
    e.g., accepts d, [a,b,c] and returns a(b(c(d)))
    """
    if len(names) > 0:
        name = names[0]
        rest = names[1:]
        return Call(name.clone(), [call_chain(inner_name, rest)])
    else:
        return inner_name.clone()
            
class FixClassdecorator(fixer_base.BaseFix):

    PATTERN = """
              decorated < one_dec=decorator < any* > cls=classdef < 'class' name=any any* > > | 
              decorated < decorators < decs=decorator+ > cls=classdef < 'class' name=any any* > >
              """
    def transform(self, node, results):

        singleton = results.get("one_dec")
        decs = [results["one_dec"]] if results.get("one_dec") is not None else results["decs"]
        dec_strings = [str(dec).strip()[1:] for dec in decs]
        assign = ""
        for dec in dec_strings:
            assign += dec
            assign += "("
        assign += results["name"].value
        for dec in dec_strings:
            assign += ")"
        assign = String(results["name"].value + " = " + assign)
        assign_statement = Node(syms.simple_stmt, [assign, Newline()])
        prefix = None
        for dec in decs:
            if prefix is None:
                prefix = dec.prefix
            dec.remove()
        results["cls"].prefix = prefix
        pos = node.children.index(results["cls"]) + 1
        i = indentation(node)
        node.insert_child(pos, Leaf(token.INDENT, i))
        node.insert_child(pos, assign_statement)
