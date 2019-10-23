"""
Add 'from __future__ import absolute_import' to any file
that uses imports.
"""
from crosswind import fixer_base
from crosswind.fixer_util_3to2 import future_import
from crosswind.pygram import python_symbols as syms


class FixAbsimport(fixer_base.BaseFix):
    order = "post"
    run_order = 10

    def __init__(self, options, log):
        super(FixAbsimport, self).__init__(options, log)
        self.__abs_added = None

    def start_tree(self, tree, filename):
        super(FixAbsimport, self).start_tree(tree, filename)
        self.__abs_added = False

    def match(self, node):
        return node.type in (syms.import_name, syms.import_from) and not self.__abs_added

    def transform(self, node, results):
        try:
            future_import("absolute_import", node)
        except ValueError:
            pass
        else:
            self.__abs_added = True

    def finish_tree(self, tree, filename):
        fixer_base.BaseFix.finish_tree(self, tree, filename)
