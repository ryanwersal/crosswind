# Copyright 2007 Google, Inc. All Rights Reserved.
# Licensed to PSF under a Contributor Agreement.

"""Fixer that changes range(...) into xrange(...)."""

# Local imports
from lib2to3 import fixer_base
from lib2to3.fixer_util import Name, Call, consuming_calls
from lib2to3 import patcomp


class FixRange(fixer_base.BaseFix):

    PATTERN = """
              power<
                 (name='range') trailer< '(' args=any ')' >
              rest=any* >
              """

    def transform(self, node, results):
        return self.transform_range(node, results)

    def transform_xrange(self, node, results):
        name = results["name"]
        name.replace(Name("range", prefix=name.get_prefix()))

    def transform_range(self, node, results):
        if not self.in_special_context(node):
            range_call = Call(Name("range"), [results["args"].clone()])
            # Encase the range call in list().
            list_call = Call(Name("list"), [range_call],
                             prefix=node.get_prefix())
            # Put things that were after the range() call after the list call.
            for n in results["rest"]:
                list_call.append_child(n)
            return list_call
        return node

    P1 = "power< func=NAME trailer< '(' node=any ')' > any* >"
    p1 = patcomp.compile_pattern(P1)

    P2 = """for_stmt< 'for' any 'in' node=any ':' any* >
            | comp_for< 'for' any 'in' node=any any* >
            | comparison< any 'in' node=any any*>
         """
    p2 = patcomp.compile_pattern(P2)

    def in_special_context(self, node):
        if node.parent is None:
            return False
        results = {}
        if (node.parent.parent is not None and
               self.p1.match(node.parent.parent, results) and
               results["node"] is node):
            # list(d.keys()) -> list(d.keys()), etc.
            return results["func"].value in consuming_calls
        # for ... in d.iterkeys() -> for ... in d.keys(), etc.
        return self.p2.match(node.parent, results) and results["node"] is node
