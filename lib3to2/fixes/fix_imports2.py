from fix_imports import FixImports
from lib2to3.fixer_util import Dot, Name

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
                if node.value + u'.' + attr.value == name:
                    results[name].append(node)
    for name in results:
        # Only return a True-like object if we have found something
        if results[name]:
            return results
    return False


class FixImports2(FixImports):
    
    mapping = MAPPING
    python2_modules = PY2MODULES

    # This should be run pretty late, as it scans the whole code.
    run_order = 7

    # Avoid working with the whole tree all of the time

    def start_tree(self, tree, filename):
        """This is only run once; we want to remember the first node"""
        super(FixImports2, self).start_tree(tree, filename)
        self.run_once = True
        self.relevant_leaves = find_relevant_leaves(tree, self.mapping)

    def name_replacing(self, module_name):
        """
        -Accepts the module name to be replaced
        -Returns a dict mapping modules to replace module_name with the
        specific usages that replace it
        -Currently relies on the caller to remove duplicate entries
        """
        relevant_leaves = self.relevant_leaves
        results = {}
        for candidate in self.mapping[module_name]:
            results[candidate] = []
            for node in relevant_leaves[module_name]:
                attr = attr_used(node)
                if attr:
                    attr = attr_used(attr)
                    if attr and attr.value in python2_modules[candidate]:
                        results[candidate].append(attr)
            return results

    def match(self, node):
        return self.run_once and self.relevant_leaves

    def transform(self, node, results):
        self.run_once = False
        relevant_leaves = self.relevant_leaves
        # Stub
