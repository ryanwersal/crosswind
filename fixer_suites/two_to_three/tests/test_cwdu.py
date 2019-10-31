import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(two_to_three_test_case):
    return two_to_three_test_case("getcwdu")


def test_basic(fixer):
    b = """os.getcwdu"""
    a = """os.getcwd"""
    fixer.check(b, a)

    b = """os.getcwdu()"""
    a = """os.getcwd()"""
    fixer.check(b, a)

    b = """meth = os.getcwdu"""
    a = """meth = os.getcwd"""
    fixer.check(b, a)

    b = """os.getcwdu(args)"""
    a = """os.getcwd(args)"""
    fixer.check(b, a)


def test_comment(fixer):
    b = """os.getcwdu() # Foo"""
    a = """os.getcwd() # Foo"""
    fixer.check(b, a)


def test_unchanged(fixer):
    s = """os.getcwd()"""
    fixer.unchanged(s)

    s = """getcwdu()"""
    fixer.unchanged(s)

    s = """os.getcwdb()"""
    fixer.unchanged(s)


def test_indentation(fixer):
    b = """
        if 1:
            os.getcwdu()
        """
    a = """
        if 1:
            os.getcwd()
        """
    fixer.check(b, a)


def test_multilation(fixer):
    b = """os .getcwdu()"""
    a = """os .getcwd()"""
    fixer.check(b, a)

    b = """os.  getcwdu"""
    a = """os.  getcwd"""
    fixer.check(b, a)

    b = """os.getcwdu (  )"""
    a = """os.getcwd (  )"""
    fixer.check(b, a)
