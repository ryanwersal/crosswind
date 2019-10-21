from .util import FixerTestCase


class Test_renames(FixerTestCase):
    fixer = "renames"

    modules = {"sys": ("maxint", "maxsize")}

    def test_import_from(self):
        for mod, (old, new) in list(self.modules.items()):
            b = "from %s import %s" % (mod, old)
            a = "from %s import %s" % (mod, new)
            self.check(b, a)

            s = "from foo import %s" % old
            self.unchanged(s)

    def test_import_from_as(self):
        for mod, (old, new) in list(self.modules.items()):
            b = "from %s import %s as foo_bar" % (mod, old)
            a = "from %s import %s as foo_bar" % (mod, new)
            self.check(b, a)

    def test_import_module_usage(self):
        for mod, (old, new) in list(self.modules.items()):
            b = """
                import %s
                foo(%s, %s.%s)
                """ % (
                mod,
                mod,
                mod,
                old,
            )
            a = """
                import %s
                foo(%s, %s.%s)
                """ % (
                mod,
                mod,
                mod,
                new,
            )
            self.check(b, a)

    def XXX_test_from_import_usage(self):
        # not implemented yet
        for mod, (old, new) in list(self.modules.items()):
            b = """
                from %s import %s
                foo(%s, %s)
                """ % (
                mod,
                old,
                mod,
                old,
            )
            a = """
                from %s import %s
                foo(%s, %s)
                """ % (
                mod,
                new,
                mod,
                new,
            )
            self.check(b, a)
