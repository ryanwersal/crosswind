import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(defuturize_test_case):
    return defuturize_test_case("standard_library")


def test_removes_standard_library_aliases(fixer):
    b = "from future import standard_library\nstandard_library.install_aliases()"
    a = "\n"
    fixer.check(b, a)


def test_removes_standard_library_but_leaves_prior_lines(fixer):
    b = "# comment\nfrom future import standard_library"
    a = "# comment\n"
    fixer.check(b, a)


def test_removes_standard_library_but_leaves_trailing_lines(fixer):
    b = "from future import standard_library\n# comment"
    a = "\n# comment"
    fixer.check(b, a)
