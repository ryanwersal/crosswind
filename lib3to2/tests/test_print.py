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
    def test_3(self):
        b = """import .dinosaur.skull
               import sys
               print #check it out!
                     (skull.jaw, skull.jaw.biteforce, file=sys.stderr)
            """
        a = """from __future__ import print_function
               import .dinosaur.skull
               import sys
               print #check it out!
                     (skull.jaw, skull.jaw.biteforce, file=sys.stderr)
            """
        self.check(b, a)
