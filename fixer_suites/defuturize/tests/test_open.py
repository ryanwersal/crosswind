import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(defuturize_test_case):
    return defuturize_test_case("open")


def test_remove_builtin_import_single(fixer):
    b = "from io import open"
    a = ""
    fixer.check(b, a)


# FIXME: This should probably be supported.
# def test_remove_builtin_imports_multiple(fixer):
#     b = "from io import BytesIO, open, StringIO"
#     a = ""
#     fixer.check(b, a)


def test_removes_builtin_import_but_leaves_prior_lines(fixer):
    b = "# comment\nfrom io import open"
    a = "# comment\n"
    fixer.check(b, a)


def test_removes_builtin_import_but_leaves_trailing_lines(fixer):
    b = "from io import open\n# comment"
    a = "\n# comment"
    fixer.check(b, a)
