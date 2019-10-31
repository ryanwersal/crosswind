from crosswind.tests.support import FixerTestCase

from .util import ImportsFixerTests


class Test_imports(FixerTestCase, ImportsFixerTests):
    fixer = "imports"
    from ..fixes.fix_imports import MAPPING as modules

    def test_multiple_imports(self):
        b = """import urlparse, cStringIO"""
        a = """import urllib.parse, io"""
        self.check(b, a)

    def test_multiple_imports_as(self):
        b = """
            import copy_reg as bar, HTMLParser as foo, urlparse
            s = urlparse.spam(bar.foo())
            """
        a = """
            import copyreg as bar, html.parser as foo, urllib.parse
            s = urllib.parse.spam(bar.foo())
            """
        self.check(b, a)
