# Python imports
from itertools import chain

# Local imports
from crosswind.tests import support


class FixerTestCase(support.TestCase):
    fixer = None

    # Other test cases can subclass this class and replace "fixer_pkg" with
    # their own.
    def setUp(self, fix_list=None, fixer_pkg="fixer_suites.two_to_three", options=None):
        if fix_list is None:
            if self.fixer is None:
                raise "'fixer' must be specified for each FixerTestCase"

            fix_list = [self.fixer]
        self.refactor = support.get_refactorer(fixer_pkg, fix_list, options)
        self.fixer_log = []
        self.filename = "<string>"

        for fixer in chain(self.refactor.pre_order, self.refactor.post_order):
            fixer.log = self.fixer_log

    def _check(self, before, after):
        before = support.reformat(before)
        after = support.reformat(after)
        tree = self.refactor.refactor_string(before, self.filename)
        self.assertEqual(after, str(tree))
        return tree

    def check(self, before, after, ignore_warnings=False):
        tree = self._check(before, after)
        self.assertTrue(tree.was_changed)
        if not ignore_warnings:
            self.assertEqual(self.fixer_log, [])

    def warns(self, before, after, message, unchanged=False):
        tree = self._check(before, after)
        self.assertIn(message, "".join(self.fixer_log))
        if not unchanged:
            self.assertTrue(tree.was_changed)

    def warns_unchanged(self, before, message):
        self.warns(before, before, message, unchanged=True)

    def unchanged(self, before, ignore_warnings=False):
        self._check(before, before)
        if not ignore_warnings:
            self.assertEqual(self.fixer_log, [])

    def assert_runs_after(self, *names):
        fixes = [self.fixer]
        fixes.extend(names)
        r = support.get_refactorer("fixer_suites.two_to_three", fixes)
        (pre, post) = r.get_fixers()
        n = "fix_" + self.fixer
        if post and post[-1].__class__.__module__.endswith(n):
            # We're the last fixer to run
            return
        if pre and pre[-1].__class__.__module__.endswith(n) and not post:
            # We're the last in pre and post is empty
            return
        self.fail(
            "Fixer run order (%s) is incorrect; %s should be last."
            % (", ".join([x.__class__.__module__ for x in (pre + post)]), n)
        )


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
