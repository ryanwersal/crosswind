import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(three_to_two_test_case):
    return three_to_two_test_case("printfunction")


def test_generic(fixer):
    b = """print()"""
    a = """from __future__ import print_function\nprint()"""
    fixer.check(b, a)


def test_literal(fixer):
    b = """print('spam')"""
    a = """from __future__ import print_function\nprint('spam')"""
    fixer.check(b, a)


def test_not_builtin_unchanged(fixer):
    s = "this.shouldnt.be.changed.because.it.isnt.builtin.print()"
    fixer.unchanged(s)


# XXX: Quoting this differently than triple-quotes, because with newline
# XXX: setting, I can't quite get the triple-quoted versions to line up.
def test_arbitrary_printing(fixer):
    b = "import dinosaur.skull\nimport sys\nprint" "(skull.jaw, skull.jaw.biteforce, file=sys.stderr)"
    a = (
        "from __future__ import print_function\n"
        "import dinosaur.skull\nimport sys\nprint"
        "(skull.jaw, skull.jaw.biteforce, file=sys.stderr)"
    )
    fixer.check(b, a)


def test_long_arglist(fixer):
    b = (
        "print(spam, spam, spam, spam, spam, baked_beans, spam, spam,"
        "spam, spam, sep=', spam, ', end=wonderful_spam)\nprint()"
    )
    a = (
        "from __future__ import print_function\n"
        "print(spam, spam, spam, spam, spam, baked_beans, spam, spam,"
        "spam, spam, sep=', spam, ', end=wonderful_spam)\nprint()"
    )
    fixer.check(b, a)
