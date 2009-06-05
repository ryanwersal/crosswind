from lib3to2.tests.test_all_fixers import lib3to2FixerTestCase

class Test_print(lib3to2FixerTestCase):
    fixer = "print"
    
    def test_1(self):
        b = """print()"""
        a = """from __future__ import print_function\nprint()"""
        self.check(b,a)
    def test_2(self):
        b = """why().print()"""
        self.unchanged(b)
    #XXX: Quoting this differently than triple-quotes, because with newline
    #XXX: setting, I can't quite get the triple-quoted versions to line up.
    def test_3(self):
        b = "import dinosaur.skull\nimport sys\nprint"\
            "(skull.jaw, skull.jaw.biteforce, file=sys.stderr)"
        a = "from __future__ import print_function\n"\
            "import dinosaur.skull\nimport sys\nprint"\
            "(skull.jaw, skull.jaw.biteforce, file=sys.stderr)"
        self.check(b, a)
    def test_4(self):
        b = "print(spam, spam, spam, spam, spam, baked_beans, spam, spam,"\
            "spam, spam, sep=', spam, ', end=wonderful_spam)\nprint()"
        a = "from __future__ import print_function\n"\
            "print(spam, spam, spam, spam, spam, baked_beans, spam, spam,"\
            "spam, spam, sep=', spam, ', end=wonderful_spam)\nprint()"
        self.check(b, a)
