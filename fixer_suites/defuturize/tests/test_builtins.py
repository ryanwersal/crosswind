import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(defuturize_test_case):
    return defuturize_test_case("builtins")


def test_remove_builtin_import_single(fixer):
    b = "from builtins import foo"
    a = ""
    fixer.check(b, a)


def test_remove_builtin_imports_multiple(fixer):
    b = "from builtins import foo, bar, baz"
    a = ""
    fixer.check(b, a)


def test_removes_all_builtin_imports(fixer):
    b = "from builtins import foo\nfrom builtins import bar\nfrom builtins import baz"
    a = "\n\n"
    fixer.check(b, a)


def test_removes_builtin_import_but_leaves_prior_lines(fixer):
    b = "# comment\nfrom builtins import foo"
    a = "# comment\n"
    fixer.check(b, a)


def test_removes_builtin_import_but_leaves_trailing_lines(fixer):
    b = "from builtins import foo\n# comment"
    a = "\n# comment"
    fixer.check(b, a)
