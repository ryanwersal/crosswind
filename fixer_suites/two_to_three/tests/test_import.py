import os

from .util import FixerTestCase


class Test_import(FixerTestCase):
    fixer = "import"

    def setUp(self):
        super(Test_import, self).setUp()
        # Need to replace fix_import's exists method
        # so we can check that it's doing the right thing
        self.files_checked = []
        self.present_files = set()
        self.always_exists = True

        def fake_exists(name):
            self.files_checked.append(name)
            return self.always_exists or (name in self.present_files)

        from ..fixes import fix_import

        fix_import.exists = fake_exists

    def tearDown(self):
        from ..fixes import fix_import

        fix_import.exists = os.path.exists

    def check_both(self, b, a):
        self.always_exists = True
        super(Test_import, self).check(b, a)
        self.always_exists = False
        super(Test_import, self).unchanged(b)

    def test_files_checked(self):
        def p(path):
            # Takes a unix path and returns a path with correct separators
            return os.path.pathsep.join(path.split("/"))

        self.always_exists = False
        self.present_files = set(["__init__.py"])
        expected_extensions = (".py", os.path.sep, ".pyc", ".so", ".sl", ".pyd")
        names_to_test = (p("/spam/eggs.py"), "ni.py", p("../../shrubbery.py"))

        for name in names_to_test:
            self.files_checked = []
            self.filename = name
            self.unchanged("import jam")

            if os.path.dirname(name):
                name = os.path.dirname(name) + "/jam"
            else:
                name = "jam"
            expected_checks = set(name + ext for ext in expected_extensions)
            expected_checks.add("__init__.py")

            self.assertEqual(set(self.files_checked), expected_checks)

    def test_not_in_package(self):
        s = "import bar"
        self.always_exists = False
        self.present_files = set(["bar.py"])
        self.unchanged(s)

    def test_with_absolute_import_enabled(self):
        s = "from __future__ import absolute_import\nimport bar"
        self.always_exists = False
        self.present_files = set(["__init__.py", "bar.py"])
        self.unchanged(s)

    def test_in_package(self):
        b = "import bar"
        a = "from . import bar"
        self.always_exists = False
        self.present_files = set(["__init__.py", "bar.py"])
        self.check(b, a)

    def test_import_from_package(self):
        b = "import bar"
        a = "from . import bar"
        self.always_exists = False
        self.present_files = set(["__init__.py", "bar" + os.path.sep])
        self.check(b, a)

    def test_already_relative_import(self):
        s = "from . import bar"
        self.unchanged(s)

    def test_comments_and_indent(self):
        b = "import bar # Foo"
        a = "from . import bar # Foo"
        self.check(b, a)

    def test_from(self):
        b = "from foo import bar, baz"
        a = "from .foo import bar, baz"
        self.check_both(b, a)

        b = "from foo import bar"
        a = "from .foo import bar"
        self.check_both(b, a)

        b = "from foo import (bar, baz)"
        a = "from .foo import (bar, baz)"
        self.check_both(b, a)

    def test_dotted_from(self):
        b = "from green.eggs import ham"
        a = "from .green.eggs import ham"
        self.check_both(b, a)

    def test_from_as(self):
        b = "from green.eggs import ham as spam"
        a = "from .green.eggs import ham as spam"
        self.check_both(b, a)

    def test_import(self):
        b = "import foo"
        a = "from . import foo"
        self.check_both(b, a)

        b = "import foo, bar"
        a = "from . import foo, bar"
        self.check_both(b, a)

        b = "import foo, bar, x"
        a = "from . import foo, bar, x"
        self.check_both(b, a)

        b = "import x, y, z"
        a = "from . import x, y, z"
        self.check_both(b, a)

    def test_import_as(self):
        b = "import foo as x"
        a = "from . import foo as x"
        self.check_both(b, a)

        b = "import a as b, b as c, c as d"
        a = "from . import a as b, b as c, c as d"
        self.check_both(b, a)

    def test_local_and_absolute(self):
        self.always_exists = False
        self.present_files = set(["foo.py", "__init__.py"])

        s = "import foo, bar"
        self.warns_unchanged(s, "absolute and local imports together")

    def test_dotted_import(self):
        b = "import foo.bar"
        a = "from . import foo.bar"
        self.check_both(b, a)

    def test_dotted_import_as(self):
        b = "import foo.bar as bang"
        a = "from . import foo.bar as bang"
        self.check_both(b, a)

    def test_prefix(self):
        b = """
        # prefix
        import foo.bar
        """
        a = """
        # prefix
        from . import foo.bar
        """
        self.check_both(b, a)
