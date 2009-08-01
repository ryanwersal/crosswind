from fix_imports import FixImports

python2_modules = { 
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
                    'StringIO', 'URLError', 'UnknownHandler', '__version__',
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
                'SimpleDialog' : (
                    'ACTIVE', 'ALL', 'ANCHOR', 'ARC', 'At', 'AtEnd', 'AtInsert',
                    'AtSelFirst', 'AtSelLast', 'BASELINE', 'BEVEL', 'BOTH',
                    'BOTTOM', 'BROWSE', 'BUTT', 'BaseWidget', 'BitmapImage',
                    'BooleanType', 'BooleanVar', 'BufferType',
                    'BuiltinFunctionType', 'BuiltinMethodType', 'Button',
                    'CASCADE', 'CENTER', 'CHAR', 'CHECKBUTTON', 'CHORD',
                    'COMMAND', 'CURRENT', 'CallWrapper', 'Canvas',
                    'Checkbutton', 'ClassType', 'CodeType', 'ComplexType',
                    'DISABLED', 'DOTBOX', 'DictProxyType', 'DictType',
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
                    'SOLID', 'SUNKEN', 'SW', 'Scale', 'Scrollbar',
                    'SimpleDialog', 'SliceType', 'Spinbox', 'StringType',
                    'StringTypes', 'StringVar', 'Studbutton', 'TOP', 'TRUE',
                    'Tcl', 'TclError', 'TclVersion', 'Text', 'Tk', 'TkVersion',
                    'Toplevel', 'TracebackType', 'Tributton', 'TupleType',
                    'TypeType', 'UNDERLINE', 'UNITS', 'UnboundMethodType',
                    'UnicodeType', 'VERTICAL', 'Variable', 'W', 'WORD',
                    'WRITABLE', 'Widget', 'Wm', 'X', 'XRangeType', 'Y', 'YES',
                    'getboolean', 'getdouble', 'getint', 'image_names',
                    'image_types', 'mainloop', 'sys', 'tkinter', 'wantobjects'),
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
                    'SimpleXMLRPCServer', 'SocketServer', '__builtins__',
                    '__doc__', '__file__', '__name__', '__package__', 'fcntl',
                    'list_public_methods', 'os', 'remove_duplicates',
                    'resolve_dotted_attribute', 'sys', 'traceback',
                    'xmlrpclib'),
                }

MAPPING = { 'urllib.request' :
                ('urllib', 'urllib2'),
            'urllib.error' :
                ('urllib', 'urllib2'),
            'urllib.parse' :
                ('urllib', 'urllib2'),
            'dbm.__init__' :
                ('anydbm', 'whichdb'),
            'http.server' :
                ('BaseHTTPServer', 'CGIHTTPServer', 'SimpleHTTPServer'),
            'tkinter.filedialog' :
                ('FileDialog', 'tkFileDialog'),
            'tkinter.simpledialog' :
                ('SimpleDialog', 'tkSimpleDialog'),
            'xmlrpc.server' :
                ('DocXMLRPCServer', 'SimpleXMLRPCServer'),
            }


        
class FixImports2(FixImports):
    pass
