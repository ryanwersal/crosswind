from crosswind.tests.support import FixerTestCase


class Test_metaclass(FixerTestCase):

    fixer = "metaclass"

    def test_unchanged(self):
        self.unchanged("class X(): pass")
        self.unchanged("class X(object): pass")
        self.unchanged("class X(object1, object2): pass")
        self.unchanged("class X(object1, object2, object3): pass")
        self.unchanged("class X(metaclass=Meta): pass")
        self.unchanged("class X(b, arg=23, metclass=Meta): pass")
        self.unchanged("class X(b, arg=23, metaclass=Meta, other=42): pass")

        s = """
        class X:
            def __metaclass__(self): pass
        """
        self.unchanged(s)

        s = """
        class X:
            a[23] = 74
        """
        self.unchanged(s)

    def test_comments(self):
        b = """
        class X:
            # hi
            __metaclass__ = AppleMeta
        """
        a = """
        class X(metaclass=AppleMeta):
            # hi
            pass
        """
        self.check(b, a)

        b = """
        class X:
            __metaclass__ = Meta
            # Bedtime!
        """
        a = """
        class X(metaclass=Meta):
            pass
            # Bedtime!
        """
        self.check(b, a)

    def test_meta(self):
        # no-parent class, odd body
        b = """
        class X():
            __metaclass__ = Q
            pass
        """
        a = """
        class X(metaclass=Q):
            pass
        """
        self.check(b, a)

        # one parent class, no body
        b = """class X(object): __metaclass__ = Q"""
        a = """class X(object, metaclass=Q): pass"""
        self.check(b, a)

        # one parent, simple body
        b = """
        class X(object):
            __metaclass__ = Meta
            bar = 7
        """
        a = """
        class X(object, metaclass=Meta):
            bar = 7
        """
        self.check(b, a)

        b = """
        class X:
            __metaclass__ = Meta; x = 4; g = 23
        """
        a = """
        class X(metaclass=Meta):
            x = 4; g = 23
        """
        self.check(b, a)

        # one parent, simple body, __metaclass__ last
        b = """
        class X(object):
            bar = 7
            __metaclass__ = Meta
        """
        a = """
        class X(object, metaclass=Meta):
            bar = 7
        """
        self.check(b, a)

        # redefining __metaclass__
        b = """
        class X():
            __metaclass__ = A
            __metaclass__ = B
            bar = 7
        """
        a = """
        class X(metaclass=B):
            bar = 7
        """
        self.check(b, a)

        # multiple inheritance, simple body
        b = """
        class X(clsA, clsB):
            __metaclass__ = Meta
            bar = 7
        """
        a = """
        class X(clsA, clsB, metaclass=Meta):
            bar = 7
        """
        self.check(b, a)

        # keywords in the class statement
        b = """class m(a, arg=23): __metaclass__ = Meta"""
        a = """class m(a, arg=23, metaclass=Meta): pass"""
        self.check(b, a)

        b = """
        class X(expression(2 + 4)):
            __metaclass__ = Meta
        """
        a = """
        class X(expression(2 + 4), metaclass=Meta):
            pass
        """
        self.check(b, a)

        b = """
        class X(expression(2 + 4), x**4):
            __metaclass__ = Meta
        """
        a = """
        class X(expression(2 + 4), x**4, metaclass=Meta):
            pass
        """
        self.check(b, a)

        b = """
        class X:
            __metaclass__ = Meta
            save.py = 23
        """
        a = """
        class X(metaclass=Meta):
            save.py = 23
        """
        self.check(b, a)
