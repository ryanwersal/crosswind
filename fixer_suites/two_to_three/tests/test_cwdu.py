from crosswind.tests.support import FixerTestCase


class Test_getcwdu(FixerTestCase):

    fixer = "getcwdu"

    def test_basic(self):
        b = """os.getcwdu"""
        a = """os.getcwd"""
        self.check(b, a)

        b = """os.getcwdu()"""
        a = """os.getcwd()"""
        self.check(b, a)

        b = """meth = os.getcwdu"""
        a = """meth = os.getcwd"""
        self.check(b, a)

        b = """os.getcwdu(args)"""
        a = """os.getcwd(args)"""
        self.check(b, a)

    def test_comment(self):
        b = """os.getcwdu() # Foo"""
        a = """os.getcwd() # Foo"""
        self.check(b, a)

    def test_unchanged(self):
        s = """os.getcwd()"""
        self.unchanged(s)

        s = """getcwdu()"""
        self.unchanged(s)

        s = """os.getcwdb()"""
        self.unchanged(s)

    def test_indentation(self):
        b = """
            if 1:
                os.getcwdu()
            """
        a = """
            if 1:
                os.getcwd()
            """
        self.check(b, a)

    def test_multilation(self):
        b = """os .getcwdu()"""
        a = """os .getcwd()"""
        self.check(b, a)

        b = """os.  getcwdu"""
        a = """os.  getcwd"""
        self.check(b, a)

        b = """os.getcwdu (  )"""
        a = """os.getcwd (  )"""
        self.check(b, a)
