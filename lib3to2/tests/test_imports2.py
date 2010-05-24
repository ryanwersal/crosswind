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
        
    def test_nested_import_all(self):
        
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

    def test_nested_import_named(self):

        b = """
        with open('myFile', 'r') as myFile:
            from urllib.request import install_opener, urlretrieve
            fileList = [ln for ln in myFile]"""
        a = """
        with open('myFile', 'r') as myFile:
            from urllib import urlretrieve
            from urllib2 import install_opener
            fileList = [ln for ln in myFile]"""
        self.check(b, a, ignore_warnings=True)

    def test_alt_wording(self):

        b = """
        if spam.is_good():
            from urllib import request, parse
            request.urlopen(spam_site)
            parse.urlencode(spam_site)"""
        a = """
        if spam.is_good():
            import urllib
            import urllib2
            urllib2.urlopen(spam_site)
            urllib.urlencode(spam_site)"""
        self.check(b, a)

    def test_simplest_usage(self):

        b = """
        import urllib.request
        urllib.request.urlopen(spam)"""

        a = """
        import urllib2
        urllib2.urlopen(spam)"""

        self.check(b, a)
