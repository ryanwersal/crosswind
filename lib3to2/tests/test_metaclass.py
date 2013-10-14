from lib3to2.tests.support import lib3to2FixerTestCase

class Test_metaclass(lib3to2FixerTestCase):

    fixer = u'metaclass'

    def test_unchanged(self):
        self.unchanged(u"class X(): pass")
        self.unchanged(u"class X(object): pass")
        self.unchanged(u"class X(object1, object2): pass")
        self.unchanged(u"class X(object1, object2, object3): pass")

        s = u"""
        class X():
            def __metaclass__(self): pass
        """
        self.unchanged(s)

        s = u"""
        class X():
            a[23] = 74
        """
        self.unchanged(s)

    def test_comments(self):
        a = u"""
        class X(object):
            # hi
            __metaclass__ = AppleMeta
            pass
        """
        b = u"""
        class X(metaclass=AppleMeta):
            # hi
            pass
        """
        self.check(b, a)

        a = u"""
        class X(object):
            __metaclass__ = Meta
            pass
            # Bedtime!
        """
        b = u"""
        class X(metaclass=Meta):
            pass
            # Bedtime!
        """
        self.check(b, a)

    def test_meta_noparent_odd_body(self):
        # no-parent class, odd body
        a = u"""
        class X(object):
            __metaclass__ = Q
            pass
        """
        b = u"""
        class X(metaclass=Q):
            pass
        """
        self.check(b, a)

    def test_meta_oneparent_no_body(self):
        # one parent class, no body
        a = u"""
        class X(object):
            __metaclass__ = Q
            pass"""
        b = u"""
        class X(object, metaclass=Q): pass"""
        self.check(b, a)

    def test_meta_oneparent_simple_body_1(self):
        # one parent, simple body
        a = u"""
        class X(object):
            __metaclass__ = Meta
            bar = 7
        """
        b = u"""
        class X(object, metaclass=Meta):
            bar = 7
        """
        self.check(b, a)

    def test_meta_oneparent_simple_body_2(self):
        a = u"""
        class X(object):
            __metaclass__ = Meta
            x = 4; g = 23
        """
        b = u"""
        class X(metaclass=Meta):
            x = 4; g = 23
        """
        self.check(b, a)

    def test_meta_oneparent_simple_body_3(self):
        a = u"""
        class X(object):
            __metaclass__ = Meta
            bar = 7
        """
        b = u"""
        class X(object, metaclass=Meta):
            bar = 7
        """
        self.check(b, a)

    def test_meta_multiparent_simple_body_1(self):
        # multiple inheritance, simple body
        a = u"""
        class X(clsA, clsB):
            __metaclass__ = Meta
            bar = 7
        """
        b = u"""
        class X(clsA, clsB, metaclass=Meta):
            bar = 7
        """
        self.check(b, a)

    def test_meta_multiparent_simple_body_2(self):
        # keywords in the class statement
        a = u"""
        class m(a, arg=23):
            __metaclass__ = Meta
            pass"""
        b = u"""
        class m(a, arg=23, metaclass=Meta):
            pass"""
        self.check(b, a)

    def test_meta_expression_simple_body_1(self):
        a = u"""
        class X(expression(2 + 4)):
            __metaclass__ = Meta
            pass
        """
        b = u"""
        class X(expression(2 + 4), metaclass=Meta):
            pass
        """
        self.check(b, a)

    def test_meta_expression_simple_body_2(self):
        a = u"""
        class X(expression(2 + 4), x**4):
            __metaclass__ = Meta
            pass
        """
        b = u"""
        class X(expression(2 + 4), x**4, metaclass=Meta):
            pass
        """
        self.check(b, a)

    def test_meta_noparent_simple_body(self):

        a = u"""
        class X(object):
            __metaclass__ = Meta
            save.py = 23
            out = 5
        """
        b = u"""
        class X(metaclass=Meta):
            save.py = 23
            out = 5
        """
        self.check(b, a)
