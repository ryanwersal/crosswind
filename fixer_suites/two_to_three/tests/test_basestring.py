from crosswind.tests.support import FixerTestCase


class Test_basestring(FixerTestCase):
    fixer = "basestring"

    def test_basestring(self):
        b = """isinstance(x, basestring)"""
        a = """isinstance(x, str)"""
        self.check(b, a)

    def test_isinstance_basestring_tuple(self):
        b = "isinstance(x, (basestring, dict))"
        a = "isinstance(x, (str, dict))"
        self.check(b, a)

        b = "isinstance(x, (dict, basestring))"
        a = "isinstance(x, (dict, str))"
        self.check(b, a)

    def test_isinstance_basestring_list(self):
        b = "isinstance(x, [basestring, dict])"
        a = "isinstance(x, [str, dict])"
        self.check(b, a)

        b = "isinstance(x, [dict, basestring])"
        a = "isinstance(x, [dict, str])"
        self.check(b, a)

    def test_ensure_past_builtins_basestring_unchanged(self):
        u = "from past.builtins import basestring"
        self.unchanged(u)

    def test_does_not_change_basestring_in_string(self):
        u = 'print("hello basestring")'
        self.unchanged(u)

    def test_does_not_change_basestring_in_methodname(self):
        u = "return encode_basestring('foo')"
        self.unchanged(u)

    def test_does_not_change_variable_assignments(self):
        u = "basestring = str"
        self.unchanged(u)
