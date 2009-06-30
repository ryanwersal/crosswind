from test_all_fixers import lib3to2FixerTestCase

class Test_raise(lib3to2FixerTestCase):

    fixer = 'raise'

    def test_unchanged(self):
        """
        Due to raise E(V) being valid in 2.5, this fixer fortunately doesn't
        need to touch code that constructs exception objects without explicit
        tracebacks.
        """
        
        s = """raise E(V)"""
        self.unchanged(s)

        s = """raise"""
        self.unchanged(s)

    def test_TODO_make_these_tests_fail(self):
        """
        These tests should fail, but don't.  TODO: Uncomment successfully.
        One potential way of making these work is a separate fix_exceptions
        with a lower run order than fix_raise, to communicate to fix_raise how
        to sort out that third argument.
        """
        
        b = """
        E = BaseException(V).with_traceback(T)
        raise E
        """
        
        #a = """
        #E = BaseException(V)
        #raise E, V, T
        #"""
        
        #self.check(b, a)
        self.unchanged(b)
        
        b = """
        E = BaseException(V)
        E.__traceback__ = S
        E.__traceback__ = T
        raise E
        """
        
        #a = """
        #E = Exception(V)
        #raise E, V, T
        
        #self.check(b, a)
        self.unchanged(b)
        

    def test_traceback(self):
        """
        This stuff currently works, and is the opposite counterpart to the
        2to3 version of fix_raise.
        """
        b = """raise E(V).with_traceback(T)"""
        a = """raise E, V, T"""
        self.check(b, a)
        
        b = """raise E().with_traceback(T)"""
        a = """raise E, None, T"""
        self.check(b, a)
