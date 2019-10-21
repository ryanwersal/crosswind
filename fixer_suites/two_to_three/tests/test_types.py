from .util import FixerTestCase


class Test_types(FixerTestCase):
    fixer = "types"

    def test_basic_types_convert(self):
        b = """types.StringType"""
        a = """bytes"""
        self.check(b, a)

        b = """types.DictType"""
        a = """dict"""
        self.check(b, a)

        b = """types . IntType"""
        a = """int"""
        self.check(b, a)

        b = """types.ListType"""
        a = """list"""
        self.check(b, a)

        b = """types.LongType"""
        a = """int"""
        self.check(b, a)

        b = """types.NoneType"""
        a = """type(None)"""
        self.check(b, a)

        b = "types.StringTypes"
        a = "(str,)"
        self.check(b, a)
