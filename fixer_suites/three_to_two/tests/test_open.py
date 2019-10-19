from .support import crosswindFixerTestCase


class Test_open(crosswindFixerTestCase):
    fixer = "open"

    def test_imports(self):
        b = """new_file = open("some_filename", newline="\\r")"""
        a = """from io import open\nnew_file = open("some_filename", newline="\\r")"""
        self.check(b, a)

    def test_doesnt_import(self):
        s = """new_file = nothing.open("some_filename")"""
        self.unchanged(s)
