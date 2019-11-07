import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(defuturize_test_case):
    return defuturize_test_case("past")


def test_warns_on_past_usage(fixer):
    u = "from past.foo import bar"
    fixer.warns_unchanged(u, "'bar' imported from past.foo")
