"""Fix renamed imports and module references."""

import re

from lib2to3.pygram import python_symbols as syms
from lib2to3.pytree import Node
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

    def find_usage(self, node, ref):
        """Returns an object in node's children that is equivalent to ref"""
        for child in node.pre_order():
            # Discard differences in prefixes
            ref.prefix = child.prefix
            if child == ref:
                return child

    # TODO: Add support for fixing later usage for name_import cases.
    def match_dotted(self, node):
        """Iterate through names matching the dotted ones"""
        results = {"node": node}
        matched = []
        for name in self.mapping.keys():
            if '.' in name:
                attrs = [Name(attr) for attr in name.split('.')]
                import_mod = self.find_usage(node, DottedName(name.split('.')))
                if import_mod:
                    import_mod.value = name
                    results["module_name"] = import_mod
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

    def match(self, node):
        return super(FixImports, self).match(node) or self.match_dotted(node)
