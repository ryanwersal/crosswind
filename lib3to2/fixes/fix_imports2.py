"""
Fixer for complicated imports
"""

from lib2to3 import fixer_base
from lib2to3.fixer_util import Name, FromImport, Newline
from ..fixer_util import token, syms, Leaf, Node, Star, \
                         import_binding_scope, indentation

TK_BASE_NAMES = ('ACTIVE', 'ALL', 'ANCHOR', 'ARC','BASELINE', 'BEVEL', 'BOTH',
                 'BOTTOM', 'BROWSE', 'BUTT', 'CASCADE', 'CENTER', 'CHAR',
                 'CHECKBUTTON', 'CHORD', 'COMMAND', 'CURRENT', 'DISABLED',
                 'DOTBOX', 'E', 'END', 'EW', 'EXCEPTION', 'EXTENDED', 'FALSE',
                 'FIRST', 'FLAT', 'GROOVE', 'HIDDEN', 'HORIZONTAL', 'INSERT',
                 'INSIDE', 'LAST', 'LEFT', 'MITER', 'MOVETO', 'MULTIPLE', 'N',
                 'NE', 'NO', 'NONE', 'NORMAL', 'NS', 'NSEW', 'NUMERIC', 'NW',
                 'OFF', 'ON', 'OUTSIDE', 'PAGES', 'PIESLICE', 'PROJECTING',
                 'RADIOBUTTON', 'RAISED', 'READABLE', 'RIDGE', 'RIGHT',
                 'ROUND', 'S', 'SCROLL', 'SE', 'SEL', 'SEL_FIRST', 'SEL_LAST',
                 'SEPARATOR', 'SINGLE', 'SOLID', 'SUNKEN', 'SW', 'StringTypes',
                 'TOP', 'TRUE', 'TclVersion', 'TkVersion', 'UNDERLINE', 
                 'UNITS', 'VERTICAL', 'W', 'WORD', 'WRITABLE', 'X', 'Y', 'YES',
                 'wantobjects')

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
                  'StringIO', 'URLError', 'UnknownHandler', 'addinfourl',
                  'build_opener', 'install_opener', 'parse_http_list',
                  'parse_keqv_list', 'randombytes', 'request_host', 'urlopen'),
              'urllib' : (
                  'ContentTooShortError', 'FancyURLopener','URLopener',
                  'basejoin', 'ftperrors', 'getproxies',
                  'getproxies_environment', 'localhost', 'pathname2url',
                  'quote', 'quote_plus', 'splitattr', 'splithost',
                  'splitnport', 'splitpasswd', 'splitport', 'splitquery',
                  'splittag', 'splittype', 'splituser', 'splitvalue',
                  'thishost', 'unquote', 'unquote_plus', 'unwrap',
                  'url2pathname', 'urlcleanup', 'urlencode', 'urlopen',
                  'urlretrieve',),
              'urlparse' : (
                  'parse_qs', 'parse_qsl', 'urldefrag', 'urljoin',
                  'urlparse', 'urlsplit', 'urlunparse', 'urlunsplit'),
              'anydbm' : (
                  'error', 'open'),
              'whichdb' : (
                  'whichdb',),
              'BaseHTTPServer' : (
                  'BaseHTTPRequestHandler', 'HTTPServer'),
              'CGIHTTPServer' : (
                  'CGIHTTPRequestHandler',),
              'SimpleHTTPServer' : (
                  'SimpleHTTPRequestHandler',),
              'FileDialog' : TK_BASE_NAMES + (
                  'FileDialog', 'LoadFileDialog', 'SaveFileDialog',
                  'dialogstates', 'test'),
              'tkFileDialog' : (
                  'Directory', 'Open', 'SaveAs', '_Dialog', 'askdirectory',
                  'askopenfile', 'askopenfilename', 'askopenfilenames',
                  'askopenfiles', 'asksaveasfile', 'asksaveasfilename'),
              'SimpleDialog' : TK_BASE_NAMES + (
                  'SimpleDialog',),
              'tkSimpleDialog' : TK_BASE_NAMES + (
                  'askfloat', 'askinteger', 'askstring', 'Dialog'),
              'SimpleXMLRPCServer' : (
                  'CGIXMLRPCRequestHandler', 'SimpleXMLRPCDispatcher',
                  'SimpleXMLRPCRequestHandler', 'SimpleXMLRPCServer',
                  'list_public_methods', 'remove_duplicates',
                  'resolve_dotted_attribute'),
              'DocXMLRPCServer' : (
                  'DocCGIXMLRPCRequestHandler', 'DocXMLRPCRequestHandler',
                  'DocXMLRPCServer', 'ServerHTMLDoc','XMLRPCDocGenerator'),
                }

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

# helps match 'http', as in 'from http.server import ...'
simple_name = "name='{name}'"
# helps match 'server', as in 'from http.server import ...'
simple_attr = "attr='{attr}'"
# helps match 'HTTPServer', as in 'from http.server import HTTPServer'
simple_using = "using='{using}'"
# helps match 'urllib.request', as in 'import urllib.request'
dotted_name = "dotted_name=dotted_name< {fmt_name} '.' {fmt_attr} >"
# helps match 'http.server', as in 'http.server.HTTPServer(...)'
power_twoname = "power< {fmt_name} trailer< '.' {fmt_attr} > [trailer< '.' using=any >] any* >"
# helps match 'from http.server import HTTPServer'
from_import_1 = "from_import=import_from< 'from' {fmt_name} 'import' {fmt_using} > | from_import=import_from< 'from' {fmt_name} 'import' import_as_name< {fmt_using} 'as' renamed=any > >"
# helps match 'from http.server import HTTPServer, SimpleHTTPRequestHandler'
# also helps match 'from http.server import *'
from_import_n = "from_import=import_from< 'from' {fmt_name} 'import' in_list=import_as_names< using=any* > > | from_import=import_from< 'from' {fmt_name} 'import' using='*' >"
# helps match 'from http import server'
mod_import = "from_import_submod=import_from< 'from' {fmt_name} 'import' {fmt_attr} > | from_import_submod=import_from< 'from' {fmt_name} 'import' import_as_name< {fmt_attr} 'as' renamed=any > > | from_import_submod=import_from< 'from' {fmt_name} 'import' in_list=import_as_names< any* {fmt_attr} any* > > | from_import_submod=import_from< 'from' {fmt_name} 'import' in_list=import_as_names< any* import_as_name< {fmt_attr} 'as' renamed=any > any* > >"
# helps match 'import urllib.request'
name_import = "name_import=import_name< 'import' {fmt_name} > | name_import=import_name< 'import' dotted_as_name< {fmt_name} 'as' renamed=any > > | name_import=import_name< 'import' dotted_as_names< any* in_list=dotted_as_name< {fmt_name} > any* > > | name_import=import_name< 'import' dotted_as_names< any* in_list=dotted_as_name< {fmt_name} 'as' renamed=any > any* > >"

def all_candidates(name, attr, MAPPING=MAPPING):
    """
    Returns all candidate packages for the name.attr
    """
    dotted = name + '.' + attr
    assert dotted in MAPPING, "No matching package found."
    return MAPPING[dotted]

def new_package(name, attr, using, MAPPING=MAPPING, PY2MODULES=PY2MODULES):
    """
    Returns which candidate package for name.attr provides using
    """
    for candidate in all_candidates(name, attr, MAPPING):
        if using in PY2MODULES[candidate]:
            break
    else:
        candidate = None

    return candidate

def build_import_pattern(mapping1, mapping2):
    """
    mapping1: A dict mapping py3k modules to all possible py2k replacements
    mapping2: A dict mapping py2k modules to the things they do
    This builds a HUGE pattern to match all ways that things can be imported
    """
    pats = []
    # py3k: urllib.request, py2k: ('urllib2', 'urllib')
    for py3k, py2k in mapping1.items():
        name, attr = py3k.split('.')
        s_name = simple_name.format(name=name)
        s_attr = simple_attr.format(attr=attr)
        d_name = dotted_name.format(fmt_name=s_name, fmt_attr=s_attr)
        # import urllib.request
        yield name_import.format(fmt_name=d_name)
        # from urllib import [spam, spam, ...,] request[, spam, spam...]
        yield mod_import.format(fmt_name=s_name, fmt_attr=s_attr)
        yield from_import_n.format(fmt_name=d_name)
        for candidate in py2k:
            for using in mapping2[candidate]:
                s_using = simple_using.format(using=using)
                # from urllib.request import ..., urlretrieve, ...
                yield from_import_1.format(fmt_name=d_name, fmt_using=s_using)

class FixImports2(fixer_base.BaseFix):

    explicit = True # Doesn't do much yet

    PATTERN = " | \n".join(build_import_pattern(MAPPING, PY2MODULES))

    def transform(self, node, results):
        """Stub"""
        name = results.get("name")
        attr = results.get("attr")
        using = results.get("using")
        in_list = results.get("in_list")
        simple_stmt = node.parent
        parent = simple_stmt.parent
        if using is None:
            #################################################
            # "from urllib import request", or              #
            # "import urllib.request"                       #
            # We have to work to figure out what to import. #
            # We need to examine each statement affected.   #
            #################################################

            for statement_affected in import_binding_scope(node):
                #################################################
                # Each node here can be affected by the import. #
                # Check to see which ones use names imported.   #
                # Fix them to the corresponding Python 2 names. #
                # Keep track of what we fix.                    #
                #################################################
                pass # TODO: STUB

        elif in_list:
            ##########################################################
            # "from urllib.request import urlopen, urlretrieve, ..." #
            # Replace one import statement with potentially many.    #
            ##########################################################
            idx = parent.children.index(simple_stmt)
            packages = dict([(n,[]) for n in all_candidates(name.value,
                                                            attr.value)])
            for imported in using:
                if imported.type == token.COMMA:
                    continue
                if imported.type == syms.import_as_name:
                    test_name = imported.children[0].value
                    rename = len(imported.children) > 2 and \
                                 imported.children[2].value
                else:
                    test_name = imported.value
                    rename = False
                pkg = new_package(name.value, attr.value, test_name)
                packages[pkg].append((test_name, rename))

            ##############################################
            # Remove the offending import statement.     #
            # Replace it with what is needed to satisfy. #
            ##############################################

        elif using.type == token.STAR:
            idx = parent.children.index(simple_stmt)
            nodes = [FromImport(pkg, [Star(prefix=' ')]) for pkg in \
                                        all_candidates(name.value, attr.value)]
            node.replace(nodes.pop())
            indent = indentation(simple_stmt)
            while nodes:
                next_stmt = Node(syms.simple_stmt, [nodes.pop(), Newline()])
                parent.insert_child(idx+1, next_stmt)
                parent.insert_child(idx+1, Leaf(token.INDENT, indent))
        else:
            pkg = new_package(name.value, attr.value, using.value)
            node.replace(FromImport(pkg, [using]))

