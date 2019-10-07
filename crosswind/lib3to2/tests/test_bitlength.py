from crosswind.lib3to2.tests.support import crosswindFixerTestCase

class Test_bitlength(crosswindFixerTestCase):
    fixer = 'bitlength'

    def test_fixed(self):
        b = """a = something.bit_length()"""
        a = """a = (len(bin(something)) - 2)"""
        self.check(b, a, ignore_warnings=True)

    def test_unfixed(self):
        s = """a = bit_length(fire)"""
        self.unchanged(s)

        s = """a = s.bit_length('some_arg')"""
        self.unchanged(s)
