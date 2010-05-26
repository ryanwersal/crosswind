"""
Fixer for complicated imports
"""

from lib2to3 import fixer_base
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
              'SimpleDialog' : ('SimpleDialog',),
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

###############################################################
# TODO                                                   TODO #
#                                                             #
#       Just import these from fix_imports, though it's       #
#       very convenient to reference them from here...        #
#                                                             #
# TODO                                                   TODO #
###############################################################

# helps match 'queue', as in 'from queue import ...'
simple_name_match = "name='{name}'"
# helps match 'client', to be used if client has been imported from http
subname_match = "attr='{attr}'"
# helps match 'HTTPConnection', as in 'http.client.HTTPConnection'
using_match = "using='{using}'"
# helps match 'http.client', as in 'import urllib.request'
dotted_name_match = "dotted_name=dotted_name< {fmt_name} '.' {fmt_attr} >"
# helps match 'http.client', as in 'http.client.HTTPConnection(...)'
power_twoname_match = "power< {fmt_name} trailer< '.' {fmt_attr} > [trailer< '.' {fmt_using} >] any* >"
# helps match 'client.HTTPConnection', if 'client' has been imported from http
power_subname_match = "power< {fmt_attr} trailer< '.' {fmt_using} > any* >"
# helps match 'from http.client import HTTPConnection'
from_import_match = "from_import=import_from< 'from' {fmt_name} 'import' {fmt_using} > | from_import=import_from< 'from' {fmt_name} 'import' import_as_name< {fmt_using} 'as' renamed=any > > | from_import=import_from< 'from' {fmt_name} 'import' in_list=import_as_names< any* {fmt_using} any* > > | from_import=import_from< 'from' {fmt_name} 'import' in_list=import_as_names< any* import_as_name< {fmt_using} 'as' renamed=any > any* > > | from_import=import_from< 'from' {fmt_name} 'import' all='*' >"
# helps match 'from http import client'
from_import_submod_match = "from_import_submod=import_from< 'from' {fmt_name} 'import' {fmt_attr} > | from_import_submod=import_from< 'from' {fmt_name} 'import' import_as_name< {fmt_attr} 'as' renamed=any > > | from_import_submod=import_from< 'from' {fmt_name} 'import' in_list=import_as_names< any* {fmt_attr} any* > > | from_import_submod=import_from< 'from' {fmt_name} 'import' in_list=import_as_names< any* import_as_name< {fmt_attr} 'as' renamed=any > any* > >"
# helps match 'import urllib.request'
name_import_match = "name_import=import_name< 'import' {fmt_name} > | name_import=import_name< 'import' dotted_as_name< {fmt_name} 'as' renamed=any > > | name_import=import_name< 'import' dotted_as_names< any* in_list=dotted_as_name< {fmt_name} > any* > > | name_import=import_name< 'import' dotted_as_names< any* in_list=dotted_as_name< {fmt_name} 'as' renamed=any > any* > >"

def build_import_pattern(mapping1, mapping2):
    """
    mapping1: A dict mapping py3k modules to all possible py2k replacements
    mapping2: A dict mapping py2k modules to the things they do
    This builds a HUGE pattern to match all conceivable ways that things can be imported
    """
    import_pattern_builder = []
    # py3k: urllib.request, py2k: ('urllib2', 'urllib')
    for py3k, py2k in mapping1.items():
        name, attr = py3k.split('.')
        simple_name = simple_name_match.format(name=name)
        simple_attr = subname_match.format(attr=attr)
        dotted_name = dotted_name_match.format(fmt_name=simple_name, fmt_attr=simple_attr)
        # import urllib.request
        import_pattern_builder.append(name_import_match.format(fmt_name=dotted_name))
        # from urllib import [spam, spam, ...,] request[, spam, spam...]
        import_pattern_builder.append(from_import_submod_match.format(fmt_name=simple_name, fmt_attr=simple_attr))
        for candidate in py2k:
            for using in mapping2[candidate]:
                simple_using = using_match.format(using=using)
                # from urllib.request import ..., urlretrieve, ...
                import_pattern_builder.append(from_import_match.format(fmt_name=dotted_name, fmt_using=simple_using))
    return import_pattern_builder

class FixImports2(fixer_base.BaseFix):

    explicit = True # Doesn't do anything

    PATTERN = " | \n".join(build_import_pattern(MAPPING, PY2MODULES))

    def transform(self, node, results):
        """Stub"""
        print(repr(node))
