"""Fix renamed imports and module references."""

import re


from lib2to3.pgen2 import token
from lib2to3.pytree import Node, Leaf
from lib2to3.pygram import python_symbols as syms
from lib2to3.fixer_util import Name, Dot, Attr, _is_import_binding

from lib2to3.fixes.fix_imports import FixImports as FixImports_
from lib2to3.fixes.fix_imports import build_pattern

MAPPING = {'reprlib': 'repr',
           'winreg': '_winreg',
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
           #TODO: make this work
           #tkinter': 'Tkinter',
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

def pkg_name(node):
    """
    Returns a tuple of:
    (pkg, (names)) if node does "from pkg import names"
    """
    if node.type != syms.import_from: return None
    return (node.children[1], node.children[3])


def DottedName(names, prefix=u""):
    """Accepts a sequence of names; returns a DottedName that combines them"""
    children = []
    for arg in names:
        children.append(Name(arg))
        children.append(Dot())
    del children[-1]
    return Node(syms.dotted_name, children, prefix=prefix)

def dot_attr_used(node):
    """
    Accepts a node and returns a dot and the attr if that node uses an attr
    Otherwise returns None
    """
    next_of_kin = node.next_sibling
    if next_of_kin is None:
        return (None, None)
    if next_of_kin.type == syms.trailer:
        return tuple(next_of_kin.children[:2]) if \
                    next_of_kin.children[0].type == token.DOT else (None, None)
    if next_of_kin.type == token.DOT and next_of_kin.next_sibling:
        return (next_of_kin, next_of_kin.next_sibling)
    else:
        return (None, None)

class FixImports(FixImports_):

    mapping = MAPPING

    def find_node_usage(self, node, ref):
        """Returns an object in node's children that is equivalent to ref"""
        for child in node.pre_order():
            # Discard differences in prefixes
            ref.prefix = child.prefix
            if child == ref:
                return child

    def match_fromimports(self, node):
        """
        Find things like from dbm import gnu
        """
        dotted_names = [tuple(name.split('.')) for name in self.mapping if '.' in name]
        if not dotted_names: return False
        packages = {}
        for name, attr in dotted_names:
            if not name in packages:
                packages[name] = set([attr])
            else:
                packages[name].add(attr)
        matched = {'node': node, 'fromimports': []}
        for package in packages:
            for name in packages[package]:
                #XXX This will fail on things like "from dbm import gnu as g"
                if _is_import_binding(node, name, package):
                    matched['fromimports'].append(node)
        if matched['fromimports']:
            return matched
        else:
            return False

    def fix_fromimports(self, nodes):
        for node in nodes:
            pkg, name = pkg_name(node)
            mapped = pkg.value + u'.' + name.value
            repl = unicode(self.mapping[mapped])
            p = u" "
            if u'.' not in repl:
                new_node = Node(syms.import_name, [Leaf(1, u'import'),
                   Node(syms.dotted_as_name, [Leaf(1, repl, prefix=p),
                   Leaf(1, u'as', prefix=p), Leaf(1, name.value, prefix=p)])])
                node.replace(new_node)
            else:
                name.replace(Name(repl.split('.')[1], prefix=p))

    def find_dotted_name_usage(self, vals):
        """
        Find the usage of a dotted name from self.replace
        Accepts: a list generated from a node.post_order()
        """
        if not self.replace:
            return False
        names_attrs = [tuple(name.split('.')) for name in self.mapping if '.' in name]
        if not names_attrs:
            return False
        packages = {}
        for name, attr in names_attrs:
            if not unicode(name) in packages:
                packages[unicode(name)] = set([attr])
            else:
                packages[unicode(name)].add(attr)
        matched = []
        # say this next line ten times fast...
        vals = [val for val in vals if isinstance(val, Leaf)]
        for val in vals:
            if val.type == token.NAME and val.value in packages:
                dot, attr = dot_attr_used(val)
            else:
                continue
            if (dot and attr) and (attr.value in packages[val.value]) and \
               val.value + u'.' + attr.value in self.replace:
                matched.append((val,dot,attr))
            else:
                continue
        return matched

    def match_dotted(self, node):
        """Iterate through names matching the dotted ones"""
        results = {"node": node}
        matched = []
        for name in self.mapping:
            if '.' in name:
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
        return super(FixImports, self).match(node) or self.match_named(node) or \
               self.match_dotted(node) or self.match_fromimports(node)

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

    def fix_names(self, names):
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


    def transform(self, node, results):
        """
        Use the parent's transform unless we have to do our own thing.
        """
        import_mod = results.get("module_name")
        names = results.get("bare_with_attr")
        fromimports = results.get("fromimports")
        if import_mod or (names and (isinstance(names[0], Leaf))):
            return super(FixImports, self).transform(node, results)
        elif names:
            self.fix_names(names)
        elif fromimports:
            self.fix_fromimports(fromimports)
