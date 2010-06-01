from test_all_fixers import lib3to2FixerTestCase

class Test_imports2(lib3to2FixerTestCase):
    fixer = "imports2"

    def test_name_scope_def(self):

        b = """
        import urllib.request
        def importing_stuff():
            import urllib.request
            urllib.request.urlopen(stuff)
        urllib.request.urlretrieve(stuff)"""
        a = """
        import urllib
        def importing_stuff():
            import urllib2
            urllib2.urlopen(stuff)
        urllib.urlretrieve(stuff)"""
        self.check(b, a)


    if False:
        def test_name_scope_class(self):

            # This one might be impossible to implement completely.
            # It's also probably unnecessary and definitely impractical.
            # One obvious limitation is that it only could ever hope to do the
            # right thing if all the classes are defined in one module.

            b = """
            import http.server

            class StuffDoer(object):
                import http.server

                def __init__(self):
                    # class namespace search after instance namespace lookup fails
                    self.http.server.HTTPServer(('localhost','80'), http.server.SimpleHTTPRequestHandler)

            class OtherStuffDoer(StuffDoer):
                def serve(self):
                    # base class namespace search after derived class namespace lookup fails
                    self.http.server.HTTPServer(('localhost', '8080'), self.http.server.CGIHTTPRequestHandler)

            http.server.HTTPServer(('localhost', '8000'), http.server.BaseHTTPRequestHandler)"""
            a = """
            import BaseHTTPServer
            import SimpleHTTPServer

            class StuffDoer(object):

                import BaseHTTPServer
                import CGIHTTPServer

                def __init__(self):
                    # class namespace search after instance namespace lookup fails
                    self.BaseHTTPServer.HTTPServer(('localhost', '80'), SimpleHTTPServer.SimpleHTTPRequestHandler)

            class OtherStuffDoer(StuffDoer):

                def serve(self):
                    # base class namespace search after derived class namespace lookup fails
                    self.BaseHTTPServer.HTTPServer(('localhost', '8080'), self.CGIHTTPServer.CGIHTTPRequestHandler)

            BaseHTTPServer.HTTPServer(('localhost', '8080'), BaseHTTPServer.BaseHTTPRequestHandler)"""

            self.check(b, a)
    
    def test_name_scope_if(self):
        
        b = """
        if thing:
            import http.server
        elif other_thing:
            import xmlrpc.server
        if related_thing:
            myServ = http.server.HTTPServer(('localhost', '80'), http.server.CGIHTTPRequestHandler)
        elif other_related_thing:
            myServ = xmlrpc.server.SimpleXMLRPCServer(('localhost', '80'), CGIXMLRPCRequestHandler)

        # just for kicks...
        monkey_wrench_in_the_works = http.server.SimpleHTTPRequestHandler"""

        a = """
        if thing:
            import BaseHTTPServer
            import CGIHTTPServer
            import SimpleHTTPServer
        elif other_thing:
            import SimpleXMLRPCServer
        if related_thing:
            myServ = BaseHTTPServer.HTTPServer(('localhost', '80'), CGIHTTPServer.CGIHTTPRequestHandler)
        elif other_related_thing:
            myServ = SimpleXMLRPCServer.SimpleXMLRPCServer(('localhost', '80'), CGIXMLRPCRequestHandler)

        # just for kicks...
        monkey_wrench_in_the_works = SimpleHTTPServer.SimpleHTTPRequestHandler"""
        self.check(b, a)

    def test_name_scope_try_except(self):
        
        b = """
        try:
            import http.server
        except ImportError:
            import xmlrpc.server

        # some time has passed, and we know that http.server was bad.
        srv = xmlrpc.server.DocXMLRPCServer(addr, xmlrpc.server.DocCGIXMLRPCRequestHandler)

        # some more time has passed, and we know that http.server is good.
        srv = http.server.HTTPServer(addr, http.server.CGIHTTPRequestHandler)"""

        a = """
        try:
            import BaseHTTPServer
            import CGIHTTPServer
        except ImportError:
            import DocXMLRPCServer

        # some time has passed, and we know that http.server was bad.
        srv = DocXMLRPCServer.DocXMLRPCServer(addr, DocXMLRPCServer.DocCGIXMLRPCRequestHandler)

        # some more time has passed, and we know that http.server is good.
        srv = BaseHTTPServer.HTTPServer(addr, CGIHTTPServer.CGIHTTPRequestHandler)"""
        self.check(b, a)

    if False:
        def test_name_bind_try(self):
        
            # Don't expect this to work.  It requires semantics checking, and it
            # would be limited to py3k library module imports that only use a
            # subset of the members that are provided by a single py2k module.
            # self.check(b, a)

            b = """
            try:
                import http.server as s
            except ImportError:
                import xmlrpc.server as s

            srv = s.DocXMLRPCServer(addr, s.DocCGIXMLRPCRequestHandler)

            # some more time has passed, and we know that http.server is good.
            srv = s.HTTPServer(addr, s.BaseHTTPRequestHandler)"""

            a = """
            try:
                import BaseHTTPServer as s
            except ImportError:
                import DocXMLRPCServer as s

            # some time has passed, and we know that http.server was bad.
            srv = s.DocXMLRPCServer(addr, s.DocCGIXMLRPCRequestHandler)

            # some more time has passed, and we know that http.server is good.
            srv = s.HTTPServer(addr, s.BaseHTTPRequestHandler)"""
            self.check(b, a)


    def test_from_single(self):

        b = "from urllib.request import urlopen"
        a = "from urllib2 import urlopen"
        self.check(b, a)

        b = "from urllib.request import urlopen\n"\
            "from urllib.parse import urlencode"
        a = "from urllib2 import urlopen\n"\
            "from urllib import urlencode"
        self.check(b, a)

        b = "from tkinter.simpledialog import SimpleDialog"
        a = "from SimpleDialog import SimpleDialog"
        self.check(b, a)
        
    def test_from_star(self):
        
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
                from BaseHTTPServer import *
                from CGIHTTPServer import *
                from SimpleHTTPServer import *
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
            from BaseHTTPServer import *
            from CGIHTTPServer import *
            from SimpleHTTPServer import *
            test_all_imports()
        def testing_xmlrpc_server():
            from SimpleXMLRPCServer import *
            from DocXMLRPCServer import *
            test_all_imports()
        """
        self.check(b, a, ignore_warnings=True)

    def test_from_list(self):

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

    def test_modulefrom(self):

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

    def test_name_usage_simple(self):

        b = """
        import urllib.request
        urllib.request.urlopen(spam)"""

        a = """
        import urllib2
        urllib2.urlopen(spam)"""

        self.check(b, a)
