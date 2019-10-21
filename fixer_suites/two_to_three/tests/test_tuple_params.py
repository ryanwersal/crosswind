from .util import FixerTestCase


class Test_tuple_params(FixerTestCase):
    fixer = "tuple_params"

    def test_unchanged_1(self):
        s = """def foo(): pass"""
        self.unchanged(s)

    def test_unchanged_2(self):
        s = """def foo(a, b, c): pass"""
        self.unchanged(s)

    def test_unchanged_3(self):
        s = """def foo(a=3, b=4, c=5): pass"""
        self.unchanged(s)

    def test_1(self):
        b = """
            def foo(((a, b), c)):
                x = 5"""

        a = """
            def foo(xxx_todo_changeme):
                ((a, b), c) = xxx_todo_changeme
                x = 5"""
        self.check(b, a)

    def test_2(self):
        b = """
            def foo(((a, b), c), d):
                x = 5"""

        a = """
            def foo(xxx_todo_changeme, d):
                ((a, b), c) = xxx_todo_changeme
                x = 5"""
        self.check(b, a)

    def test_3(self):
        b = """
            def foo(((a, b), c), d) -> e:
                x = 5"""

        a = """
            def foo(xxx_todo_changeme, d) -> e:
                ((a, b), c) = xxx_todo_changeme
                x = 5"""
        self.check(b, a)

    def test_semicolon(self):
        b = """
            def foo(((a, b), c)): x = 5; y = 7"""

        a = """
            def foo(xxx_todo_changeme): ((a, b), c) = xxx_todo_changeme; x = 5; y = 7"""
        self.check(b, a)

    def test_keywords(self):
        b = """
            def foo(((a, b), c), d, e=5) -> z:
                x = 5"""

        a = """
            def foo(xxx_todo_changeme, d, e=5) -> z:
                ((a, b), c) = xxx_todo_changeme
                x = 5"""
        self.check(b, a)

    def test_varargs(self):
        b = """
            def foo(((a, b), c), d, *vargs, **kwargs) -> z:
                x = 5"""

        a = """
            def foo(xxx_todo_changeme, d, *vargs, **kwargs) -> z:
                ((a, b), c) = xxx_todo_changeme
                x = 5"""
        self.check(b, a)

    def test_multi_1(self):
        b = """
            def foo(((a, b), c), (d, e, f)) -> z:
                x = 5"""

        a = """
            def foo(xxx_todo_changeme, xxx_todo_changeme1) -> z:
                ((a, b), c) = xxx_todo_changeme
                (d, e, f) = xxx_todo_changeme1
                x = 5"""
        self.check(b, a)

    def test_multi_2(self):
        b = """
            def foo(x, ((a, b), c), d, (e, f, g), y) -> z:
                x = 5"""

        a = """
            def foo(x, xxx_todo_changeme, d, xxx_todo_changeme1, y) -> z:
                ((a, b), c) = xxx_todo_changeme
                (e, f, g) = xxx_todo_changeme1
                x = 5"""
        self.check(b, a)

    def test_docstring(self):
        b = """
            def foo(((a, b), c), (d, e, f)) -> z:
                "foo foo foo foo"
                x = 5"""

        a = """
            def foo(xxx_todo_changeme, xxx_todo_changeme1) -> z:
                "foo foo foo foo"
                ((a, b), c) = xxx_todo_changeme
                (d, e, f) = xxx_todo_changeme1
                x = 5"""
        self.check(b, a)

    def test_lambda_no_change(self):
        s = """lambda x: x + 5"""
        self.unchanged(s)

    def test_lambda_parens_single_arg(self):
        b = """lambda (x): x + 5"""
        a = """lambda x: x + 5"""
        self.check(b, a)

        b = """lambda(x): x + 5"""
        a = """lambda x: x + 5"""
        self.check(b, a)

        b = """lambda ((((x)))): x + 5"""
        a = """lambda x: x + 5"""
        self.check(b, a)

        b = """lambda((((x)))): x + 5"""
        a = """lambda x: x + 5"""
        self.check(b, a)

    def test_lambda_simple(self):
        b = """lambda (x, y): x + f(y)"""
        a = """lambda x_y: x_y[0] + f(x_y[1])"""
        self.check(b, a)

        b = """lambda(x, y): x + f(y)"""
        a = """lambda x_y: x_y[0] + f(x_y[1])"""
        self.check(b, a)

        b = """lambda (((x, y))): x + f(y)"""
        a = """lambda x_y: x_y[0] + f(x_y[1])"""
        self.check(b, a)

        b = """lambda(((x, y))): x + f(y)"""
        a = """lambda x_y: x_y[0] + f(x_y[1])"""
        self.check(b, a)

    def test_lambda_one_tuple(self):
        b = """lambda (x,): x + f(x)"""
        a = """lambda x1: x1[0] + f(x1[0])"""
        self.check(b, a)

        b = """lambda (((x,))): x + f(x)"""
        a = """lambda x1: x1[0] + f(x1[0])"""
        self.check(b, a)

    def test_lambda_simple_multi_use(self):
        b = """lambda (x, y): x + x + f(x) + x"""
        a = """lambda x_y: x_y[0] + x_y[0] + f(x_y[0]) + x_y[0]"""
        self.check(b, a)

    def test_lambda_simple_reverse(self):
        b = """lambda (x, y): y + x"""
        a = """lambda x_y: x_y[1] + x_y[0]"""
        self.check(b, a)

    def test_lambda_nested(self):
        b = """lambda (x, (y, z)): x + y + z"""
        a = """lambda x_y_z: x_y_z[0] + x_y_z[1][0] + x_y_z[1][1]"""
        self.check(b, a)

        b = """lambda (((x, (y, z)))): x + y + z"""
        a = """lambda x_y_z: x_y_z[0] + x_y_z[1][0] + x_y_z[1][1]"""
        self.check(b, a)

    def test_lambda_nested_multi_use(self):
        b = """lambda (x, (y, z)): x + y + f(y)"""
        a = """lambda x_y_z: x_y_z[0] + x_y_z[1][0] + f(x_y_z[1][0])"""
        self.check(b, a)
