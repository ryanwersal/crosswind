"""
Fixer for complicated imports
"""

from lib2to3 import fixer_base
from lib2to3.fixer_util import Name, String, FromImport, Newline, Comma
from ..fixer_util import token, syms, Leaf, Node, Star, indentation, ImportAsName

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

# helps match 'http', as in 'from http.server import ...'
simple_name = "name='%s'"
# helps match 'server', as in 'from http.server import ...'
simple_attr = "attr='%s'"
# helps match 'HTTPServer', as in 'from http.server import HTTPServer'
simple_using = "using='%s'"
# helps match 'urllib.request', as in 'import urllib.request'
dotted_name = "dotted_name=dotted_name< %s '.' %s >"
# helps match 'http.server', as in 'http.server.HTTPServer(...)'
power_twoname = "pow=power< %s trailer< '.' %s > trailer< '.' using=any > any* >"
# helps match 'from http.server import HTTPServer'
# also helps match 'from http.server import HTTPServer, SimpleHTTPRequestHandler'
# also helps match 'from http.server import *'
from_import = "from_import=import_from< 'from' %s 'import' (import_as_name< using=any 'as' renamed=any> | in_list=import_as_names< using=any* > | using='*' | using=NAME) >"
# helps match 'from http import server'
mod_import = "from_import_submod=import_from< 'from' %s 'import' (%s | import_as_name< %s 'as' renamed=any > | in_list=import_as_names< any* (%s | import_as_name< %s 'as' renamed=any >) any* >) >"
# helps match 'import urllib.request'
name_import = "name_import=import_name< 'import' (%s | dotted_as_name< %s 'as' renamed=any > | dotted_as_names< any* in_list=dotted_as_name< %s ['as' renamed=any] > any* >) >"

def all_modules_subpattern():
    """
    Builds a pattern for all toplevel names
    (urllib, http, etc)
    """
    names_dot_attrs = [mod.split(".") for mod in MAPPING]
    return "( " + " | ".join([dotted_name % (simple_name % (mod[0]),
                                             simple_attr % (mod[1])) for mod in names_dot_attrs]) + " )"

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
        s_name = simple_name % (name)
        s_attr = simple_attr % (attr)
        d_name = dotted_name % (s_name, s_attr)
        yield name_import % (d_name, d_name, d_name)
        yield from_import % (all_modules_subpattern())
        yield power_twoname % (s_name, s_attr)

class FixImports2(fixer_base.BaseFix):

    explicit = True

    PATTERN = " | \n".join(build_import_pattern(MAPPING, PY2MODULES))

    def transform(self, node, results):
        name = results.get("name")
        attr = results.get("attr")
        using = results.get("using")
        in_list = results.get("in_list")
        power = results.get("pow")
        simple_stmt = node.parent
        parent = simple_stmt.parent
        idx = parent.children.index(simple_stmt)
        if using is None:
            # import urllib.request
            candidates = all_candidates(name.value, attr.value)
            nodes = [Node(syms.import_name, [Name("import"), Name(c, prefix=" ")]) for c in candidates]
            replacement = nodes.pop()
            replacement.prefix = node.prefix
            node.replace(replacement)
            indent = indentation(simple_stmt)
            while nodes:
                next_stmt = Node(syms.simple_stmt, [nodes.pop(), Newline()])
                parent.insert_child(idx+1, next_stmt)
                parent.insert_child(idx+1, Leaf(token.INDENT, indent))

        elif in_list:
            ##########################################################
            # "from urllib.request import urlopen, urlretrieve, ..." #
            # Replace one import statement with potentially many.    #
            ##########################################################
            packages = dict([(n,[]) for n in all_candidates(name.value,
                                                            attr.value)])
            for imported in using:
                if imported.type == token.COMMA:
                    continue
                if imported.type == syms.import_as_name:
                    test_name = imported.children[0].value
                    if len(imported.children) > 2:
                        rename = imported.children[2].value
                    else:
                        rename = None
                else:
                    test_name = imported.value
                    rename = None
                pkg = new_package(name.value, attr.value, test_name)
                packages[pkg].append((test_name, rename))

            imports = []
            for new_pkg, names in packages.items():
                if not names:
                    continue
                new_names = []
                for test_name, rename in names:
                    if rename is None:
                        new_names.append(Name(test_name, prefix=" "))
                    else:
                        new_names.append(ImportAsName(test_name, rename, prefix=" "))
                    new_names.append(Comma())
                new_names.pop()
                imports.append(FromImport(new_pkg, new_names))
            replacement = imports.pop()
            replacement.prefix = node.prefix
            node.replace(replacement)
            indent = indentation(simple_stmt)
            while imports:
                next_stmt = Node(syms.simple_stmt, [imports.pop(), Newline()])
                parent.insert_child(idx+1, next_stmt)
                parent.insert_child(idx+1, Leaf(token.INDENT, indent))
                

            ##############################################
            # Remove the offending import statement.     #
            # Replace it with what is needed to satisfy. #
            ##############################################

        elif using.type == token.STAR:
            nodes = [FromImport(pkg, [Star(prefix=" ")]) for pkg in
                                        all_candidates(name.value, attr.value)]
            replacement = nodes.pop()
            replacement.prefix = node.prefix
            node.replace(replacement)
            indent = indentation(simple_stmt)
            while nodes:
                next_stmt = Node(syms.simple_stmt, [nodes.pop(), Newline()])
                parent.insert_child(idx+1, next_stmt)
                parent.insert_child(idx+1, Leaf(token.INDENT, indent))
        elif power is not None:
            pkg = new_package(name.value, attr.value, using.value)
            attr.parent.remove()
            name.replace(Name(pkg, prefix=name.prefix))

        else:
            pkg = new_package(name.value, attr.value, using.value)
            node.replace(FromImport(pkg, [using]))

