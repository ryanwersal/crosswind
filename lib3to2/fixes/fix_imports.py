"""Fix renamed imports and module references."""

import re

from lib2to3.pygram import python_symbols as syms
from lib2to3.pgen2 import token
from lib2to3.pytree import Node, Leaf
from lib2to3.fixer_util import Name, Dot, Attr

from lib2to3.fixes.fix_imports import FixImports as FixImports_
from lib2to3.fixes.fix_imports import build_pattern

def DottedName(names, prefix=u""):
    """Accepts a sequence of names; returns a DottedName that combines them"""
    children = []
    for arg in names:
        children.append(Name(arg))
        children.append(Dot())
    del children[-1]
    return Node(syms.dotted_name, children, prefix)

MAPPING = {'winreg': '_winreg',
           'configparser': 'ConfigParser',
           'copyreg': 'copy_reg',
           'queue': 'Queue',
           'socketserver': 'SocketServer',
           '_markupbase': 'markupbase',
           'test.support': 'test.test_support',
           'dbm.bsd': 'dbhash',
           'dbm.ndbm': 'dbm',
           'dbm.dumb': 'dumbdbm',
           'dbm.gnu': 'gdbm',
           'html.parser': 'HTMLParser',
           'html.entities': 'htmlentitydefs',
           'http.client': 'httplib',
           'http.cookies': 'Cookie',
           'http.cookiejar': 'cookielib',
           'tkinter.dialog': 'Dialog',
           'tkinter._fix': 'FixTk',
           'tkinter.scrolledtext': 'ScrolledText',
           'tkinter.tix': 'Tix',
           'tkinter.constants': 'Tkconstants',
           'tkinter.dnd': 'Tkdnd',
           'tkinter.__init__': 'Tkinter',
           'tkinter.colorchooser': 'tkColorChooser',
           'tkinter.commondialog': 'tkCommonDialog',
           'tkinter.font': 'tkFont',
           'tkinter.messagebox': 'tkMessageBox',
           'tkinter.turtle': 'turtle',
           'urllib.robotparser': 'robotparser',
           'xmlrpc.client': 'xmlrpclib',
}

class FixImports(FixImports_):

    mapping = MAPPING

    def find_node_usage(self, node, ref):
        """Returns an object in node's children that is equivalent to ref"""
        for child in node.pre_order():
            # Discard differences in prefixes
            ref.prefix = child.prefix
            if child == ref:
                return child

    def find_dotted_name_usage(self, vals):
        """
        Find the usage of a dotted name from self.replace
        Accepts: a list generated from a node.post_order()
        """
        if not self.replace:
            return False
        names_attrs = [tuple(name.split('.')) for name in self.mapping if '.' in name]
        if names_attrs:
            names, attrs = zip(*names_attrs)
        else:
            return False
        matched = []
        # say this next line ten times fast...
        vals = [val for val in vals if type(val) == Leaf]
        vals = iter(vals)
        try:
            #Do this the long way; we need to manipulate the iterator.
            while True:
                val = vals.next()
                if val.value in names:
                    dot = vals.next()
                    if dot.value != u'.':
                        val = dot
                        continue
                    attr = vals.next()
                    if val.value + u'.' + attr.value in self.replace:
                        val.named_dotted = True
                        matched.append((val,dot,attr))
                else:
                    val = vals.next()
        except StopIteration:
            return matched

    def match_dotted(self, node):
        """Iterate through names matching the dotted ones"""
        results = {"node": node}
        matched = []
        for name in self.mapping:
            if '.' in name:
                attrs = [Name(attr) for attr in name.split('.')]
                import_mod = self.find_node_usage(node, DottedName(name.split('.')))
                if import_mod:
                    import_mod.value = name
                    results["module_name"] = import_mod
                    self.replace[import_mod.value] = self.mapping[import_mod.value]
                    matched.append(import_mod)
        # This switch flags self.transform to perform certain actions
        if len(matched) == 0:
            return False
        if len(matched) == 1:
            if not re.match("from %s import +" % name, str(node)) or \
               not re.match("import * %s * as +" % name, str(node)):
                results["name_import"] = True
        else:
            results["multiple_imports"] = True
        return results

    def match_named(self, node):
        """
        Builds the results dict for self.match() based on what we get in find_dotted_name_usage
        """
        results = {"node": node}
        name_usage = self.find_dotted_name_usage(node.pre_order())
        if name_usage:
            results["bare_with_attr"] = name_usage
        else:
            return False
        return results
        
    def match(self, node):
        """
        An amalgamation of the basic matcher and our own handling of dotted modules
        """
        return super(FixImports, self).match(node) or self.match_dotted(node) or \
               self.match_named(node)

    def transform_dotted_to_single(self, old, new):
        """
        Accepts an old tuple of Leafs (Name, Dot, Name) and a string
        Replaces (Name, Dot, Name) with a single Name, from new.
        """
        old[0].replace(Name(new, prefix=old[0].prefix))
        old[1].remove()
        old[2].remove()

    def transform_dotted_to_dotted(self, old, new):
        """
        Accepts an old tuple of Leafs (Name, Dot, Name) 
        """
        old[0].replace(Name(new[0], prefix=old[0].prefix))
        old[2].replace(Name(new[1], prefix=old[2].prefix))

    def transform(self, node, results):
        """
        Use the parent's transform unless we have to do our own thing.
        """
        import_mod = results.get("module_name")
        names = results.get("bare_with_attr")
        if import_mod or (names and (type(names[0]) == Leaf)):
            return super(FixImports, self).transform(node, results)
        else:
            for name in names:
                # TODO: Fix one node at a time.
                full_name = name[0].value + name[1].value + name[2].value
                new_name = self.replace.get(full_name)
                if u'.' not in new_name:
                    self.transform_dotted_to_single(name, new_name)
                else:
                    # test.test_support and everything in fix_imports2
                    new_mod, new_attr = new_name.split('.')
                    self.transform_dotted_to_dotted(name, (new_mod, new_attr))
