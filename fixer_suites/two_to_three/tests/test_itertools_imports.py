from crosswind.tests.support import FixerTestCase


class Test_itertools_imports(FixerTestCase):
    fixer = "itertools_imports"

    def test_reduced(self):
        b = "from itertools import imap, izip, foo"
        a = "from itertools import foo"
        self.check(b, a)

        b = "from itertools import bar, imap, izip, foo"
        a = "from itertools import bar, foo"
        self.check(b, a)

        b = "from itertools import chain, imap, izip"
        a = "from itertools import chain"
        self.check(b, a)

    def test_comments(self):
        b = "#foo\nfrom itertools import imap, izip"
        a = "#foo\n"
        self.check(b, a)

    def test_none(self):
        b = "from itertools import imap, izip"
        a = ""
        self.check(b, a)

        b = "from itertools import izip"
        a = ""
        self.check(b, a)

    def test_import_as(self):
        b = "from itertools import izip, bar as bang, imap"
        a = "from itertools import bar as bang"
        self.check(b, a)

        b = "from itertools import izip as _zip, imap, bar"
        a = "from itertools import bar"
        self.check(b, a)

        b = "from itertools import imap as _map"
        a = ""
        self.check(b, a)

        b = "from itertools import imap as _map, izip as _zip"
        a = ""
        self.check(b, a)

        s = "from itertools import bar as bang"
        self.unchanged(s)

    def test_ifilter_and_zip_longest(self):
        for name in "filterfalse", "zip_longest":
            b = "from itertools import i%s" % (name,)
            a = "from itertools import %s" % (name,)
            self.check(b, a)

            b = "from itertools import imap, i%s, foo" % (name,)
            a = "from itertools import %s, foo" % (name,)
            self.check(b, a)

            b = "from itertools import bar, i%s, foo" % (name,)
            a = "from itertools import bar, %s, foo" % (name,)
            self.check(b, a)

    def test_import_star(self):
        s = "from itertools import *"
        self.unchanged(s)

    def test_unchanged(self):
        s = "from itertools import foo"
        self.unchanged(s)
