from fix_imports import FixImports, DottedName
from lib2to3.pytree import Leaf, Node
from lib2to3.fixer_util import Dot, Comma, Name, Newline, FromImport, find_root
from lib2to3.pygram import python_symbols as syms
from lib2to3.pgen2 import token

PY2MODULES = {
              'urllib2' : (
                  'AbstractBasicAuthHandler', 'AbstractDigestAuthHandler',
                  'AbstractHTTPHandler', 'BaseHandler', 'CacheFTPHandler',
                  'FTPHandler', 'FileHandler', 'HTTPBasicAuthHandler',
                  'HTTPCookieProcessor', 'HTTPDefaultErrorHandler',
                  'HTTPDigestAuthHandler', 'HTTPError', 'HTTPErrorProcessor',
                  'HTTPHandler', 'HTTPPasswordMgr',
                  'HTTPPasswordMgrWithDefaultRealm', 'HTTPRedirectHandler',
                  'HTTPSHandler', 'OpenerDirector', 'ProxyBasicAuthHandler',
                  'ProxyDigestAuthHandler', 'ProxyHandler', 'Request',
                  'StringIO', 'URLError', 'UnknownHandler',
                  '_cut_port_re', '_opener', '_parse_proxy', 'addinfourl',
                  'base64', 'bisect', 'build_opener', 'ftpwrapper',
                  'getproxies', 'hashlib', 'httplib', 'install_opener',
                  'localhost', 'mimetools', 'os', 'parse_http_list',
                  'parse_keqv_list', 'posixpath', 'quote', 'random',
                  'randombytes', 're', 'request_host', 'socket', 'splitattr',
                  'splithost', 'splitpasswd', 'splitport', 'splittype',
                  'splituser', 'splitvalue', 'sys', 'time', 'unquote',
                  'unwrap', 'url2pathname', 'urlopen', 'urlparse', ),
              'urllib' : (
                  'ContentTooShortError', 'FancyURLopener', 'MAXFTPCACHE',
                  'URLopener', '_ftperrors', '_have_ssl', '_hextochr',
                  '_hostprog', '_is_unicode', '_localhost', '_noheaders',
                  '_nportprog', '_passwdprog', '_portprog', '_queryprog',
                  '_safemaps', '_tagprog', '_thishost', '_typeprog',
                  '_urlopener', '_userprog', '_valueprog', 'addbase',
                  'addclosehook', 'addinfo', 'addinfourl', 'always_safe',
                  'basejoin', 'ftpcache', 'ftperrors', 'ftpwrapper',
                  'getproxies', 'getproxies_environment', 'localhost', 'main',
                  'noheaders', 'os', 'pathname2url', 'proxy_bypass',
                  'proxy_bypass_environment', 'quote', 'quote_plus',
                  'reporthook', 'socket', 'splitattr', 'splithost',
                  'splitnport', 'splitpasswd', 'splitport', 'splitquery',
                  'splittag', 'splittype', 'splituser', 'splitvalue', 'ssl',
                  'string', 'sys', 'test', 'test1', 'thishost', 'time',
                  'toBytes', 'unquote', 'unquote_plus', 'unwrap',
                  'url2pathname', 'urlcleanup', 'urlencode', 'urlopen',
                  'urlretrieve', 'warnings'),
              'urlparse' : (
                  'MAX_CACHE_SIZE', 'ParseResult', 'ResultMixin',
                  'SplitResult', '_hextochr', '_parse_cache', '_splitnetloc',
                  '_splitparams', 'clear_cache', 'namedtuple',
                  'non_hierarchical', 'parse_qs', 'parse_qsl', 'scheme_chars',
                  'test', 'test_input', 'unquote', 'urldefrag', 'urljoin',
                  'urlparse', 'urlsplit', 'urlunparse', 'urlunsplit',
                  'uses_fragment', 'uses_netloc', 'uses_params', 'uses_query',
                  'uses_relative'),
              'anydbm' : (
                  '_defaultmod', '_errors', '_mod', '_name', '_names',
                  'error', 'open'),
              'whichdb' : (
                  '_dbmerror', 'dbm', 'os', 'struct', 'sys', 'whichdb'),
              'BaseHTTPServer' : (
                  'BaseHTTPRequestHandler', 'DEFAULT_ERROR_CONTENT_TYPE',
                  'DEFAULT_ERROR_MESSAGE', 'HTTPServer', 'SocketServer',
                  '_quote_html', 'catch_warnings', 'filterwarnings',
                  'mimetools', 'socket', 'sys', 'test', 'time'),
              'CGIHTTPServer' : (
                  'BaseHTTPServer', 'CGIHTTPRequestHandler',
                  'SimpleHTTPServer', 'executable', 'nobody', 'nobody_uid',
                  'os', 'select', 'sys', 'test', 'urllib'),
              'SimpleHTTPServer' : (
                  'BaseHTTPServer', 'SimpleHTTPRequestHandler', 'StringIO',
                  'cgi', 'mimetypes', 'os', 'posixpath', 'shutil', 'test',
                  'urllib'),
              'FileDialog' : (
                  'ACTIVE', 'ALL', 'ANCHOR', 'ARC', 'At', 'AtEnd', 'AtInsert',
                  'AtSelFirst', 'AtSelLast', 'BASELINE', 'BEVEL', 'BOTH',
                  'BOTTOM', 'BROWSE', 'BUTT', 'BaseWidget', 'BitmapImage',
                  'BooleanType', 'BooleanVar', 'BufferType',
                  'BuiltinFunctionType', 'BuiltinMethodType', 'Button',
                  'CASCADE', 'CENTER', 'CHAR', 'CHECKBUTTON', 'CHORD',
                  'COMMAND', 'CURRENT', 'CallWrapper', 'Canvas',
                  'Checkbutton', 'ClassType', 'CodeType', 'ComplexType',
                  'DISABLED', 'DOTBOX', 'Dialog', 'DictProxyType', 'DictType',
                  'DictionaryType', 'DoubleVar', 'E', 'END', 'EW',
                  'EXCEPTION', 'EXTENDED', 'EllipsisType', 'Entry', 'Event',
                  'FALSE', 'FIRST', 'FLAT', 'FileDialog', 'FileType',
                  'FloatType', 'Frame', 'FrameType', 'FunctionType', 'GROOVE',
                  'GeneratorType', 'GetSetDescriptorType', 'Grid', 'HIDDEN',
                  'HORIZONTAL', 'INSERT', 'INSIDE', 'Image', 'InstanceType',
                  'IntType', 'IntVar', 'LAST', 'LEFT', 'Label', 'LabelFrame',
                  'LambdaType', 'ListType', 'Listbox', 'LoadFileDialog',
                  'LongType', 'MITER', 'MOVETO', 'MULTIPLE',
                  'MemberDescriptorType', 'Menu', 'Menubutton', 'Message',
                  'MethodType', 'Misc', 'ModuleType', 'N', 'NE', 'NO', 'NONE',
                  'NORMAL', 'NS', 'NSEW', 'NUMERIC', 'NW', 'NoDefaultRoot',
                  'NoneType', 'NotImplementedType', 'OFF', 'ON', 'OUTSIDE',
                  'ObjectType', 'OptionMenu', 'PAGES', 'PIESLICE',
                  'PROJECTING', 'Pack', 'PanedWindow', 'PhotoImage', 'Place',
                  'RADIOBUTTON', 'RAISED', 'READABLE', 'RIDGE', 'RIGHT',
                  'ROUND', 'Radiobutton', 'S', 'SCROLL', 'SE', 'SEL',
                  'SEL_FIRST', 'SEL_LAST', 'SEPARATOR', 'SINGLE', 'SOLID',
                  'SUNKEN', 'SW', 'SaveFileDialog', 'Scale', 'Scrollbar',
                  'SliceType', 'Spinbox', 'StringType', 'StringTypes',
                  'StringVar', 'Studbutton', 'TOP', 'TRUE', 'Tcl', 'TclError',
                  'TclVersion', 'Text', 'Tk', 'TkVersion', 'Toplevel',
                  'TracebackType', 'Tributton', 'TupleType', 'TypeType',
                  'UNDERLINE', 'UNITS', 'UnboundMethodType', 'UnicodeType',
                  'VERTICAL', 'Variable', 'W', 'WORD', 'WRITABLE', 'Widget',
                  'Wm', 'X', 'XRangeType', 'Y', 'YES', 'dialogstates',
                  'fnmatch', 'getboolean', 'getdouble', 'getint',
                  'image_names', 'image_types', 'mainloop', 'os', 'sys',
                  'test', 'tkinter', 'wantobjects'),
              'tkFileDialog' : (
                  'Dialog', 'Directory', 'Open', 'SaveAs', '_Dialog',
                  'askdirectory', 'askopenfile', 'askopenfilename',
                  'askopenfilenames', 'askopenfiles', 'asksaveasfile',
                  'asksaveasfilename'),
              # tkSimpleDialog works in every case but this one class
              'SimpleDialog' : ('SimpleDialog'),
              'tkSimpleDialog' : (
                  'ACTIVE', 'ALL', 'ANCHOR', 'ARC', 'At', 'AtEnd', 'AtInsert',
                  'AtSelFirst', 'AtSelLast', 'BASELINE', 'BEVEL', 'BOTH',
                  'BOTTOM', 'BROWSE', 'BUTT', 'BaseWidget', 'BitmapImage',
                  'BooleanType', 'BooleanVar', 'BufferType',
                  'BuiltinFunctionType', 'BuiltinMethodType', 'Button',
                  'CASCADE', 'CENTER', 'CHAR', 'CHECKBUTTON', 'CHORD',
                  'COMMAND', 'CURRENT', 'CallWrapper', 'Canvas',
                  'Checkbutton', 'ClassType', 'CodeType', 'ComplexType',
                  'DISABLED', 'DOTBOX', 'Dialog', 'DictProxyType', 'DictType',
                  'DictionaryType', 'DoubleVar', 'E', 'END', 'EW',
                  'EXCEPTION', 'EXTENDED', 'EllipsisType', 'Entry', 'Event',
                  'FALSE', 'FIRST', 'FLAT', 'FileType', 'FloatType', 'Frame',
                  'FrameType', 'FunctionType', 'GROOVE', 'GeneratorType',
                  'GetSetDescriptorType', 'Grid', 'HIDDEN', 'HORIZONTAL',
                  'INSERT', 'INSIDE', 'Image', 'InstanceType', 'IntType',
                  'IntVar', 'LAST', 'LEFT', 'Label', 'LabelFrame',
                  'LambdaType', 'ListType', 'Listbox', 'LongType', 'MITER',
                  'MOVETO', 'MULTIPLE', 'MemberDescriptorType', 'Menu',
                  'Menubutton', 'Message', 'MethodType', 'Misc', 'ModuleType',
                  'N', 'NE', 'NO', 'NONE', 'NORMAL', 'NS', 'NSEW', 'NUMERIC',
                  'NW', 'NoDefaultRoot', 'NoneType', 'NotImplementedType',
                  'OFF', 'ON', 'OUTSIDE', 'ObjectType', 'OptionMenu', 'PAGES',
                  'PIESLICE', 'PROJECTING', 'Pack', 'PanedWindow',
                  'PhotoImage', 'Place', 'RADIOBUTTON', 'RAISED', 'READABLE',
                  'RIDGE', 'RIGHT', 'ROUND', 'Radiobutton', 'S', 'SCROLL',
                  'SE', 'SEL', 'SEL_FIRST', 'SEL_LAST', 'SEPARATOR', 'SINGLE',
                  'SOLID', 'SUNKEN', 'SW', 'Scale', 'Scrollbar', 'SliceType',
                  'Spinbox', 'StringType', 'StringTypes', 'StringVar',
                  'Studbutton', 'TOP', 'TRUE', 'Tcl', 'TclError',
                  'TclVersion', 'Text', 'Tk', 'TkVersion', 'Toplevel',
                  'TracebackType', 'Tributton', 'TupleType', 'TypeType',
                  'UNDERLINE', 'UNITS', 'UnboundMethodType', 'UnicodeType',
                  'VERTICAL', 'Variable', 'W', 'WORD', 'WRITABLE', 'Widget',
                  'Wm', 'X', 'XRangeType', 'Y', 'YES', '_QueryDialog',
                  '_QueryFloat', '_QueryInteger', '_QueryString', 'askfloat',
                  'askinteger', 'askstring', 'getboolean', 'getdouble',
                  'getint', 'image_names', 'image_types', 'mainloop', 'sys',
                  'tkinter', 'wantobjects'),
              'DocXMLRPCServer' : (
                  'CGIXMLRPCRequestHandler', 'DocCGIXMLRPCRequestHandler',
                  'DocXMLRPCRequestHandler', 'DocXMLRPCServer',
                  'ServerHTMLDoc', 'SimpleXMLRPCRequestHandler',
                  'SimpleXMLRPCServer', 'XMLRPCDocGenerator', 'inspect',
                  'pydoc', 're', 'resolve_dotted_attribute', 'sys'),
              'SimpleXMLRPCServer' : (
                  'BaseHTTPServer', 'CGIXMLRPCRequestHandler', 'Fault',
                  'SimpleXMLRPCDispatcher', 'SimpleXMLRPCRequestHandler',
                  'SimpleXMLRPCServer', 'SocketServer', 'fcntl',
                  'list_public_methods', 'os', 'remove_duplicates',
                  'resolve_dotted_attribute', 'sys', 'traceback',
                  'xmlrpclib'),
                }


# The order of the values of each key is not arbitrary.  If multiple modules provide the same name,
# then the first module listed here will be used.
# e.g., urllib and urllib2 both provide urlopen, but since urllib2 is listed first, it will be preferred.
MAPPING = { 'urllib.request' :
                ('urllib2', 'urllib'),
            'urllib.error' :
                ('urllib2', 'urllib'),
            'urllib.parse' :
                ('urllib2', 'urllib'),
            'dbm.__init__' :
                ('anydbm', 'whichdb'),
            'http.server' :
                ('CGIHTTPServer', 'SimpleHTTPServer', 'BaseHTTPServer'),
            'tkinter.filedialog' :
                ('tkFileDialog', 'FileDialog'),
            'tkinter.simpledialog' :
                ('tkSimpleDialog', 'SimpleDialog'),
            'xmlrpc.server' :
                ('DocXMLRPCServer', 'SimpleXMLRPCServer'),
            }

def is_from_import(node):
    """Returns true if the node is a from x import y statement"""
    return node.type == syms.import_from

def is_name_import(node):
    """Returns true if the node is a import y statement."""
    return node.type == syms.import_name

def attr_used(node):
    """
    Returns the attribute of a node if it has one, None if it does not.
    Attribute must look like foo.bar, with any prefix on bar acceptable
    """
    dot = Dot()
    adj = node.next_sibling
    if adj is not None:
        dot.prefix = adj.prefix
        if dot != adj:
            return None
        next = adj.next_sibling
        return next

def names_imported_from(node):
   """
   Accepts an import_from node and returns a list of the name leafs
   that the node imports
   """
   for child in node.children:
       if child.type == syms.import_as_names:
           names = [grandchild.clone() for grandchild in child.children if grandchild.type == token.NAME]
           if child.prev_sibling.type == 7 and\
              child.next_sibling.type == 8:
               # with parens, special precautions are to be made.
               # namely, the parens need to be visible,
               # and the prefixes of all the actual names are to be set to a single space.
               for name in names:
                   name.prefix = u" "
               names.insert(0, child.prev_sibling)
               names.insert(len(names), child.next_sibling)
           return names
       elif child.type == token.NAME and \
            child.value == u'import' and \
            child.next_sibling.type == token.NAME:
           return [child.next_sibling.clone()]

def full_name(node):
    """
    Shortcut for str(name_dot_attr(node))
    """
    return node.value + u'.' + attr_used(node).value

def name_dot_attr(node):
    """
    Shortcut for (node, node.next_sibling, node.next_sibling.next_sibling)
    """
    return (node, node.next_sibling, node.next_sibling.next_sibling)

def scrub_results(results):
    """
    Deletes all keys with a val that evals to False
    """
    items = results.items()
    for key, val in items:
        if not val:
            del results[key]

def which_are_imports(relevant_leaves):
    """
    Accepts relevant_leaves and returns an object of the same structure
    that contains just those that are in import statements.
    """
    from_import = set()
    name_import = set()
    for name in relevant_leaves:
        for node in relevant_leaves[name]:
            while node.parent and not (is_name_import(node) or is_from_import(node)):
                node = node.parent
            if is_from_import(node): node._mod = name; from_import.add(node)
            elif is_name_import(node): node._mod = name; name_import.add(node)
    return (from_import, name_import)

def no_kids(node):
    for child in node.children:
        if type(child) == Leaf:
            del child
        else:
            no_kids(child)

def find_relevant_leaves(tree, mapping):
    """
    Searches through the whole tree and returns a mapping of each package in
    mapping to the nodes that include it
    """
    base_names = [name.split('.')[0] for name in mapping]
    results = {}
    for name in mapping:
        results[name] = []
    for node in tree.pre_order():
        attr = attr_used(node)
        if attr and (node.value in base_names):
            for name in mapping:
                if full_name(node) == name:
                    results[name].append(node)
    scrub_results(results)
    return results

def commatize(leafs):
    new_leafs = []
    for leaf in leafs:
        new_leafs.append(leaf)
        new_leafs.append(Comma())
    del new_leafs[-1]
    return new_leafs


class FixImports2(FixImports):

    mapping = MAPPING
    modules = PY2MODULES

    # This should be run pretty late, as it scans the whole code.
    run_order = 7

    # Avoid working with the whole tree all of the time

    def start_tree(self, tree, filename):
        """This is only run once; we want to remember the first node"""
        super(FixImports2, self).start_tree(tree, filename)
        self.run_once = True
        self.relevant_leaves = find_relevant_leaves(tree, self.mapping)

    def which_candidate(self, module_name, node):
        """
        Accepts the old module name and a node that it imports
        Returns the best module to import that node from
        """
        mapping = self.mapping
        modules = self.modules
        candidates = []
        for candidate in mapping[module_name]:
            if node.value in modules[candidate]:
                return candidate

    def match(self, node):
        return self.run_once and self.relevant_leaves

    def transform(self, node, results):
        self.run_once = False
        full_nodes = []
        relevant_leaves = self.relevant_leaves
        mapping = self.mapping
        for package in relevant_leaves:
            for leaf in relevant_leaves[package]:
                full_nodes.append(name_dot_attr(leaf))
        from_imports, name_imports = which_are_imports(relevant_leaves)
        for import_statement in name_imports:
            self.warning(import_statement, 'Import name not supported yet.  Please use from (name) import (names)')
        replacers = {}
        for import_statement in from_imports:
            if not str(import_statement) in replacers:
                replacers[str(import_statement)] = {}
            else:
                continue
            curr_replacer = replacers[str(import_statement)]
            names_imported = names_imported_from(import_statement)
            if names_imported[0].type == 7 and names_imported[-1].type == 8:
                # currently, nothing is done with the parentheses, but this opens up the possibility.
                parens = (names_imported[0].clone(), names_imported[-1].clone())
                names_imported = names_imported[1:-1]
                # if the parentheses can somehow survive in the future, take out this line:
                names_imported[0].prefix = parens[0].prefix
            else:
                parens = None
            for node_imported in names_imported:
                replacing_name = self.which_candidate(import_statement._mod, node_imported)
                if not replacing_name in curr_replacer: curr_replacer[replacing_name] = []
                curr_replacer[replacing_name].append(node_imported)
        for import_statement in from_imports:
            new_nodes = []
            for replacing_name in replacers[str(import_statement)]:
                new_nodes.append(FromImport(replacing_name, commatize([name.clone() for name in replacers[str(import_statement)][replacing_name]])))
                new_nodes.append(Newline())
            del new_nodes[-1]
            new_nodes[-1].prefix = import_statement.prefix
            no_kids(import_statement)
            assert import_statement.parent
            parent = import_statement.parent
            pos = import_statement.remove()
            for node in new_nodes[::]:
                parent.insert_child(pos, node)
