"""
Fixer to remove class decorators
"""

from lib2to3 import fixer_base
from lib2to3.fixer_util import Call, Assign

def dec_name(decorator_node):
    return decorator_node.children[1]

def get_pos(node):
    assert node.parent, repr(node)
    for i, child in enumerate(node.parent.children):
        if child is node:
            return i

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
              dec_node=decorated < dec=decorator < any* > cls=classdef < 'class' name=any any* > > | 
              dec_node=decorated < decs=decorators < any* > cls=classdef < 'class' name=any any* > >
              """

    def transform(self, node, results):
        """
        This just strips annotations from the funcdef completely.
        """
        dec_node = results["dec_node"]
        cls = results["cls"]
        name = results["name"].clone()
        name.prefix = u""
        # If there's just one decorator, put it in a list
        # Otherwise, get all the decorators into one list
        decs = [results.get("dec")] if "dec" in results else \
               [dec for dec in results.get("decs").children]
        # where to insert the new name after decorations are removed
        pos = get_pos(cls)+1
        dec_names = [dec_name(dec).clone() for dec in decs]
        for dec in decs:
            dec.remove()
        # new_name becomes first_decorator(second_decorator(...(class_name)...))
        new_name = call_chain(name, dec_names)
        new_assignment = Assign(name, new_name)
        cls.parent.insert_child(pos, new_assignment)
