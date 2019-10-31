import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(three_to_two_test_case):
    return three_to_two_test_case("print")


def test_generic(fixer):
    b = """print()"""
    a = """print"""
    fixer.check(b, a)


def test_literal(fixer):
    b = """print('spam')"""
    a = """print 'spam'"""
    fixer.check(b, a)


def test_not_builtin_unchanged(fixer):
    s = "this.shouldnt.be.changed.because.it.isnt.builtin.print()"
    fixer.unchanged(s)


# XXX: Quoting this differently than triple-quotes, because with newline
# XXX: setting, I can't quite get the triple-quoted versions to line up.
def test_arbitrary_printing(fixer):
    b = "import dinosaur.skull\nimport sys\nprint" "(skull.jaw, skull.jaw.biteforce, file=sys.stderr)"
    a = "import dinosaur.skull\nimport sys\nprint " ">>sys.stderr, skull.jaw, skull.jaw.biteforce"
    fixer.check(b, a)


def test_long_arglist(fixer):
    b = (
        "print(spam, spam, spam, spam, spam, baked_beans, spam, spam,"
        " spam, spam, sep=', spam, ', end=wonderful_spam)\nprint()"
    )
    a = (
        "import sys\nprint ', spam, '.join([unicode(spam), unicode(spam), unicode(spam), unicode(spam), unicode(spam), unicode(baked_beans),"
        " unicode(spam), unicode(spam), unicode(spam), unicode(spam)]),; sys.stdout.write(wonderful_spam)\nprint"
    )
    fixer.check(b, a, ignore_warnings=True)


def test_nones(fixer):
    b = "print(1,2,3,end=None, sep=None, file=None)"
    a = "print 1,2,3"
    fixer.check(b, a)


def test_file_arg(fixer):
    b = 'print("You must specify an input file or an input string", file=sys.stderr)'
    a = 'print >>sys.stderr, "You must specify an input file or an input string"'
    fixer.check(b, a)


def test_argument_unpacking(fixer):
    s = "print(*args)"
    fixer.warns_unchanged(
        s, "-fprint does not support argument unpacking.  fix using -xprint and then again with  -fprintfunction."
    )
