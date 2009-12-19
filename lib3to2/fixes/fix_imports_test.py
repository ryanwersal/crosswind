"""
Fixer for standard library imports renamed in Python 3
"""

from lib2to3 import fixer_base
from lib2to3.fixer_util import Name, is_probably_builtin, Newline
from lib2to3.pygram import python_symbols as syms
from lib2to3.pgen2 import token
from lib2to3.pytree import Node, Leaf

from ..fixer_util import NameImport

# used in simple_mapping_to_pattern()
MAPPING1 = {"reprlib": "repr",
            "winreg": "_winreg",
            "configparser": "ConfigParser",
            "copyreg": "copy_reg",
            "queue": "Queue",
            "socketserver": "SocketServer",
            "_markupbase": "markupbase",
            "test.support": "test.test_support",
            "dbm.bsd": "dbhash",
            "dbm.ndbm": "dbm",
            "dbm.dumb": "dumbdbm",
            "dbm.gnu": "gdbm",
            "html.parser": "HTMLParser",
            "html.entities": "htmlentitydefs",
            "http.client": "httplib",
            "http.cookies": "Cookie",
            "http.cookiejar": "cookielib",
            "tkinter": "Tkinter",
            "tkinter.dialog": "Dialog",
            "tkinter._fix": "FixTk",
            "tkinter.scrolledtext": "ScrolledText",
            "tkinter.tix": "Tix",
            "tkinter.constants": "Tkconstants",
            "tkinter.dnd": "Tkdnd",
            "tkinter.__init__": "Tkinter",

            "tkinter.colorchooser": "tkColorChooser",
            "tkinter.commondialog": "tkCommonDialog",
            "tkinter.font": "tkFont",
            "tkinter.messagebox": "tkMessageBox",
            "tkinter.turtle": "turtle",
            "urllib.robotparser": "robotparser",
            "xmlrpc.client": "xmlrpclib",
}

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
MAPPING2 = {'urllib.request' :
                ('urllib2', 'urllib'),
            'urllib.error' :
                ('urllib2', 'urllib'),
            'urllib.parse' :
                ('urllib2', 'urllib', 'urlparse'),
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

# generic strings to help build patterns
# these variables mean (with urllib.request.urlopen as an example):
# name = urllib
# attr = request
# used = urlopen
# fmt_name is a formatted subpattern (simple_name_match or dotted_name_match)

# helps match 'queue', as in 'from queue import ...'
simple_name_match = "name='{name}'"
# helps match 'request', to be used if request has been imported from urllib
subname_match = "attr='{attr}'"
# helps match 'urllib.request', as in 'import urllib.request'
dotted_name_match = "dotted_name=dotted_name< {fmt_name} '.' {fmt_attr} >"
# helps match 'queue', as in 'queue.Queue(...)'
power_onename_match = "power< {fmt_name} trailer< '.' using=NAME > any* >"
# helps match 'urllib.request', as in 'urllib.request.urlopen(...)'
power_twoname_match = "power< {fmt_name} trailer< '.' {fmt_attr} > [trailer< '.' using=NAME >] any* >"
# helps match 'request.urlopen', if 'request' has been imported from urllib
power_subname_match = "power< {fmt_attr} trailer< '.' using=NAME > any* >"
# helps match 'from urllib.request import urlopen'
from_import_match = "from_import=import_from< 'from' {fmt_name} 'import' imported=any >"
# helps match 'from urllib import request'
from_import_submod_match = "from_import_submod=import_from< 'from' {fmt_name} 'import' {fmt_attr} > | from_import_submod=import_from< 'from' {fmt_name} 'import' dotted_as_names< any* dotted_as_name< {fmt_attr} 'as' renamed=any > any* > >"
# helps match 'import urllib.request'
name_import_match = "name_import=import_name< 'import' {fmt_name} > | name_import=import_name< 'import' dotted_as_name< {fmt_name} 'as' renamed=any > >"
# helps match 'import urllib.request, winreg'
multiple_name_import_match = "name_import=import_name< 'import' dotted_as_names< any* {fmt_name} any* > > | name_import=import_name< 'import' dotted_as_names< any* dotted_as_name< {fmt_name} 'as' renamed=any > any* > >"

def all_patterns(name):
    """
    Accepts a string and returns a pattern of possible patterns involving that name
    Called by simple_mapping_to_pattern for each name in the mapping it receives.
    """

    # i_ denotes an import-like node
    # u_ denotes a node that appears to be a usage of the name
    if '.' in name:
        name, attr = name.split('.', 1)
        simple_name = simple_name_match.format(name=name)
        simple_attr = subname_match.format(attr=attr)
        dotted_name = dotted_name_match.format(fmt_name=simple_name, fmt_attr=simple_attr)
        i_from = from_import_match.format(fmt_name=dotted_name)
        i_from_submod = from_import_submod_match.format(fmt_name=simple_name, fmt_attr=simple_attr)
        i_name = name_import_match.format(fmt_name=dotted_name)
        i_name_mult = multiple_name_import_match.format(fmt_name=dotted_name)
        u_name = power_twoname_match.format(fmt_name=simple_name, fmt_attr=simple_attr)
        u_subname = power_subname_match.format(fmt_attr=simple_attr)
        return ' | \n'.join((i_name, i_from, i_from_submod, i_name_mult, u_name, u_subname))
    else:
        simple_name = simple_name_match.format(name=name)
        i_name = name_import_match.format(fmt_name=simple_name)
        i_name_mult = multiple_name_import_match.format(fmt_name=simple_name)
        i_from = from_import_match.format(fmt_name=simple_name)
        u_name = power_onename_match.format(fmt_name=simple_name)
        return ' | \n'.join((i_name, i_name_mult, i_from, u_name))


class FixImportsTest(fixer_base.BaseFix):

    simple_pattern = ' | \n'.join(all_patterns(name) for name in MAPPING1)
    PATTERN = ' | \n'.join((simple_pattern, ))

    def fix_dotted_name(self, node, mapping=MAPPING1):
        """
        Accepts either a DottedName node or a power node with a trailer.
        If mapping is given, use it; otherwise use our MAPPING1
        Returns a node that can be in-place replaced by the node given
        """
        if node.type == syms.dotted_name:
            _name = node.children[0]
            _attr = node.children[2]
            name = _name.value
            attr = _attr.value
            full_name = name + u'.' + attr
            to_repl = mapping.get(full_name)
            assert to_repl
            if u'.' in to_repl:
                repl_name, repl_attr = to_repl.split(u'.')
                _name.replace(Name(repl_name, prefix=_name.prefix))
                _attr.replace(Name(repl_attr, prefix=_attr.prefix))
            else:
                node.replace(Name(to_repl, prefix=node.prefix))

    def fix_simple_name(self, node, mapping=MAPPING1):
        """
        Accepts a Name leaf.
        If mapping is given, use it; otherwise use our MAPPING1
        Returns a node that can be in-place replaced by the node given
        """
        assert node.type == token.NAME, repr(node)
        replacement = mapping[node.value]
        node.replace(Leaf(token.NAME, unicode(replacement), prefix=node.prefix))

    def fix_submod_import(self, imported, name, node):
        """
        Accepts a list of NAME leafs, a name string, and a node
        node is given as an argument to BaseFix.transform()
        NAME leafs come from an import_as_names node (the children)
        name string is the base name found in node.
        """
        submods = []
        missed = []
        for attr in imported:
            dotted = u'.'.join((name, attr.value))
            if dotted in MAPPING1:
                # get the replacement module
                to_repl = MAPPING1[dotted]
                if '.' not in to_repl:
                    # it's a simple name, so use a simple replacement.
                    _import = NameImport(Name(to_repl, prefix=u" "), attr.value)
                    submods.append(_import)
            elif attr.type == token.NAME:
                missed.append(attr.clone())
        if not submods:
            return

        parent = node.parent
        node.replace(submods[0])
        if len(submods) > 1:
            start = submods.pop(0)
            prev = start
            for submod in submods:
                parent.append_child(submod)
        if missed:
            self.warning(node, "Imported names not known to 3to2 to be part of the package {0}.  Leaving those alone... high probability that this code will be incorrect.".format(name))
            children = [Name("from"), Name(name, prefix=u" "), Name("import", prefix=u" "), Node(syms.import_as_names, missed)]
            orig_stripped = Node(syms.import_from, children)
            parent.append_child(Newline())
            parent.append_child(orig_stripped)


    def get_dotted_replacement(self, name_node, attr_node, mapping=MAPPING1):
        full_name = name_node.value + u'.' + attr_node.value
        replacement = mapping[full_name]
        if u'.' in replacement:
            new_name, new_attr = replacement.split(u'.')
            return Name(new_name, prefix=name_node.prefix), Node(syms.dotted_as_name, [Name(new_attr, prefix=attr_node.prefix), Name(u'as', prefix=u" "), attr_node.clone()])
        else:
            return Node(syms.dotted_as_name, [Name(replacement, prefix=name_node.prefix), Name(u'as', prefix=u' '), Name(attr_node.value, prefix=attr_node.prefix)]), None
    
    def transform(self, node, results):
        a = 0
        while a < 10:
            from_import = results.get("from_import")
            from_import_submod = results.get("from_import_submod")
            name_import = results.get("name_import")
            dotted_name = results.get("dotted_name")
            name = results.get("name")
            attr = results.get("attr")
            imported = results.get("imported")
            if from_import_submod:
                new_name, new_attr = self.get_dotted_replacement(name, attr)
                if new_attr is not None:
                    name.replace(new_name)
                    attr.replace(new_attr)
                else:
                    children = [Name("import"), new_name]
                    node.replace(Node(syms.import_name, children, prefix=node.prefix))
                    break
            elif dotted_name:
                self.fix_dotted_name(dotted_name)
            elif node.type == syms.power:
                pass
            elif name:
                self.fix_simple_name(name)
            elif imported and imported.type == syms.import_as_names:
                self.fix_submod_import(imported=imported.children, node=node, name=name.value)

            results = self.match(node)
            if not results:
                break
            else:
                a += 1
