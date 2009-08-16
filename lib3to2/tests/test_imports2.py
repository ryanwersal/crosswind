from test_all_fixers import lib3to2FixerTestCase

class Test_imports2(lib3to2FixerTestCase):
    fixer = "imports2"

    def test_simple_imports(self):

        b = "from urllib.request import urlopen"
        a = "from urllib2 import urlopen"
        self.check(b, a)

        b = "from urllib.request import urlopen\n"\
            "from urllib.parse import urlencode"
        a = "from urllib2 import urlopen\n"\
            "from urllib import urlencode"
        self.check(b, a)

        b = "from tkinter.simpledialog import Grid, SimpleDialog"
        a = "from tkSimpleDialog import Grid\n"\
            "from SimpleDialog import SimpleDialog"
        self.check(b, a)
        
    def test_nested_imports(self):
        
        b = """
        def try_import(package):
            try:
                from http.server import *
                print('success')
            except ImportError:
                print('failure', end="")
                print('try again!')
        """
        a = """
        def try_import(package):
            try:
                from CGIHTTPServer import *
                from SimpleHTTPServer import *
                from BaseHTTPServer import *
                print('success')
            except ImportError:
                print('failure', end="")
                print('try again!')
        """
        self.check(b, a, ignore_warnings=True)
        
        b = """
        def testing_http_server():
            from http.server import *
            test_all_imports()
        def testing_xmlrpc_server():
            from xmlrpc.server import *
            test_all_imports()
        """
        a = """
        def testing_http_server():
            from CGIHTTPServer import *
            from SimpleHTTPServer import *
            from BaseHTTPServer import *
            test_all_imports()
        def testing_xmlrpc_server():
            from SimpleXMLRPCServer import *
            from DocXMLRPCServer import *
            test_all_imports()
        """
        self.check(b, a, ignore_warnings=True)
        
        
