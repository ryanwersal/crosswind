from .util import FixerTestCase


class Test_execfile(FixerTestCase):
    fixer = "execfile"

    def test_conversion(self):
        b = """execfile("fn")"""
        a = """exec(compile(open("fn", "rb").read(), "fn", 'exec'))"""
        self.check(b, a)

        b = """execfile("fn", glob)"""
        a = """exec(compile(open("fn", "rb").read(), "fn", 'exec'), glob)"""
        self.check(b, a)

        b = """execfile("fn", glob, loc)"""
        a = """exec(compile(open("fn", "rb").read(), "fn", 'exec'), glob, loc)"""
        self.check(b, a)

        b = """execfile("fn", globals=glob)"""
        a = """exec(compile(open("fn", "rb").read(), "fn", 'exec'), globals=glob)"""
        self.check(b, a)

        b = """execfile("fn", locals=loc)"""
        a = """exec(compile(open("fn", "rb").read(), "fn", 'exec'), locals=loc)"""
        self.check(b, a)

        b = """execfile("fn", globals=glob, locals=loc)"""
        a = """exec(compile(open("fn", "rb").read(), "fn", 'exec'), globals=glob, locals=loc)"""
        self.check(b, a)

    def test_spacing(self):
        b = """execfile( "fn" )"""
        a = """exec(compile(open( "fn", "rb" ).read(), "fn", 'exec'))"""
        self.check(b, a)

        b = """execfile("fn",  globals = glob)"""
        a = """exec(compile(open("fn", "rb").read(), "fn", 'exec'),  globals = glob)"""
        self.check(b, a)
