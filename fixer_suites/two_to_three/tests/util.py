# Python imports
from itertools import chain


class ImportsFixerTests:
    # Dummy fields that will be overridden in subclasses.
    modules = None

    def check(self, x, y):
        pass

    def unchanged(self, _):
        pass

    def test_import_module(self):
        for old, new in self.modules.items():
            b = "import %s" % old
            a = "import %s" % new
            self.check(b, a)

            b = "import foo, %s, bar" % old
            a = "import foo, %s, bar" % new
            self.check(b, a)

    def test_import_from(self):
        for old, new in self.modules.items():
            b = "from %s import foo" % old
            a = "from %s import foo" % new
            self.check(b, a)

            b = "from %s import foo, bar" % old
            a = "from %s import foo, bar" % new
            self.check(b, a)

            b = "from %s import (yes, no)" % old
            a = "from %s import (yes, no)" % new
            self.check(b, a)

    def test_import_module_as(self):
        for old, new in self.modules.items():
            b = "import %s as foo_bar" % old
            a = "import %s as foo_bar" % new
            self.check(b, a)

            b = "import %s as foo_bar" % old
            a = "import %s as foo_bar" % new
            self.check(b, a)

    def test_import_from_as(self):
        for old, new in self.modules.items():
            b = "from %s import foo as bar" % old
            a = "from %s import foo as bar" % new
            self.check(b, a)

    def test_star(self):
        for old, new in self.modules.items():
            b = "from %s import *" % old
            a = "from %s import *" % new
            self.check(b, a)

    def test_import_module_usage(self):
        for old, new in self.modules.items():
            b = """
                import %s
                foo(%s.bar)
                """ % (
                old,
                old,
            )
            a = """
                import %s
                foo(%s.bar)
                """ % (
                new,
                new,
            )
            self.check(b, a)

            b = """
                from %s import x
                %s = 23
                """ % (
                old,
                old,
            )
            a = """
                from %s import x
                %s = 23
                """ % (
                new,
                old,
            )
            self.check(b, a)

            s = """
                def f():
                    %s.method()
                """ % (
                old,
            )
            self.unchanged(s)

            # test nested usage
            b = """
                import %s
                %s.bar(%s.foo)
                """ % (
                old,
                old,
                old,
            )
            a = """
                import %s
                %s.bar(%s.foo)
                """ % (
                new,
                new,
                new,
            )
            self.check(b, a)

            b = """
                import %s
                x.%s
                """ % (
                old,
                old,
            )
            a = """
                import %s
                x.%s
                """ % (
                new,
                old,
            )
            self.check(b, a)
