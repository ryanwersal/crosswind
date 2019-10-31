import os

import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(two_to_three_test_case, monkeypatch):
    test_case = two_to_three_test_case("import")
    test_case.files_checked = []
    test_case.present_files = set()
    test_case.always_exists = True

    def fake_exists(name):
        test_case.files_checked.append(name)
        return test_case.always_exists or (name in test_case.present_files)

    from ..fixes import fix_import

    monkeypatch.setattr(fix_import, "exists", fake_exists)

    return test_case


def check_both(fixer, b, a):
    fixer.always_exists = True
    fixer.check(b, a)
    fixer.always_exists = False
    fixer.unchanged(b)


def test_files_checked(fixer):
    def p(path):
        # Takes a unix path and returns a path with correct separators
        return os.path.pathsep.join(path.split("/"))

    fixer.always_exists = False
    fixer.present_files = set(["__init__.py"])
    expected_extensions = (".py", os.path.sep, ".pyc", ".so", ".sl", ".pyd")
    names_to_test = (p("/spam/eggs.py"), "ni.py", p("../../shrubbery.py"))

    for name in names_to_test:
        fixer.files_checked = []
        fixer.filename = name
        fixer.unchanged("import jam")

        if os.path.dirname(name):
            name = os.path.dirname(name) + "/jam"
        else:
            name = "jam"
        expected_checks = set(name + ext for ext in expected_extensions)
        expected_checks.add("__init__.py")

        assert set(fixer.files_checked) == expected_checks


def test_not_in_package(fixer):
    s = "import bar"
    fixer.always_exists = False
    fixer.present_files = set(["bar.py"])
    fixer.unchanged(s)


def test_with_absolute_import_enabled(fixer):
    s = "from __future__ import absolute_import\nimport bar"
    fixer.always_exists = False
    fixer.present_files = set(["__init__.py", "bar.py"])
    fixer.unchanged(s)


def test_in_package(fixer):
    b = "import bar"
    a = "from . import bar"
    fixer.always_exists = False
    fixer.present_files = set(["__init__.py", "bar.py"])
    fixer.check(b, a)


def test_import_from_package(fixer):
    b = "import bar"
    a = "from . import bar"
    fixer.always_exists = False
    fixer.present_files = set(["__init__.py", "bar" + os.path.sep])
    fixer.check(b, a)


def test_already_relative_import(fixer):
    s = "from . import bar"
    fixer.unchanged(s)


def test_comments_and_indent(fixer):
    b = "import bar # Foo"
    a = "from . import bar # Foo"
    fixer.check(b, a)


def test_from(fixer):
    b = "from foo import bar, baz"
    a = "from .foo import bar, baz"
    check_both(fixer, b, a)

    b = "from foo import bar"
    a = "from .foo import bar"
    check_both(fixer, b, a)

    b = "from foo import (bar, baz)"
    a = "from .foo import (bar, baz)"
    check_both(fixer, b, a)


def test_dotted_from(fixer):
    b = "from green.eggs import ham"
    a = "from .green.eggs import ham"
    check_both(fixer, b, a)


def test_from_as(fixer):
    b = "from green.eggs import ham as spam"
    a = "from .green.eggs import ham as spam"
    check_both(fixer, b, a)


def test_import(fixer):
    b = "import foo"
    a = "from . import foo"
    check_both(fixer, b, a)

    b = "import foo, bar"
    a = "from . import foo, bar"
    check_both(fixer, b, a)

    b = "import foo, bar, x"
    a = "from . import foo, bar, x"
    check_both(fixer, b, a)

    b = "import x, y, z"
    a = "from . import x, y, z"
    check_both(fixer, b, a)


def test_import_as(fixer):
    b = "import foo as x"
    a = "from . import foo as x"
    check_both(fixer, b, a)

    b = "import a as b, b as c, c as d"
    a = "from . import a as b, b as c, c as d"
    check_both(fixer, b, a)


def test_local_and_absolute(fixer):
    fixer.always_exists = False
    fixer.present_files = set(["foo.py", "__init__.py"])

    s = "import foo, bar"
    fixer.warns_unchanged(s, "absolute and local imports together")


def test_dotted_import(fixer):
    b = "import foo.bar"
    a = "from . import foo.bar"
    check_both(fixer, b, a)


def test_dotted_import_as(fixer):
    b = "import foo.bar as bang"
    a = "from . import foo.bar as bang"
    check_both(fixer, b, a)


def test_prefix(fixer):
    b = """
    # prefix
    import foo.bar
    """
    a = """
    # prefix
    from . import foo.bar
    """
    check_both(fixer, b, a)
