import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(two_to_three_test_case):
    return two_to_three_test_case("tuple_params")


def test_unchanged_1(fixer):
    s = """def foo(): pass"""
    fixer.unchanged(s)


def test_unchanged_2(fixer):
    s = """def foo(a, b, c): pass"""
    fixer.unchanged(s)


def test_unchanged_3(fixer):
    s = """def foo(a=3, b=4, c=5): pass"""
    fixer.unchanged(s)


def test_1(fixer):
    b = """
        def foo(((a, b), c)):
            x = 5"""

    a = """
        def foo(xxx_todo_changeme):
            ((a, b), c) = xxx_todo_changeme
            x = 5"""
    fixer.check(b, a)


def test_2(fixer):
    b = """
        def foo(((a, b), c), d):
            x = 5"""

    a = """
        def foo(xxx_todo_changeme, d):
            ((a, b), c) = xxx_todo_changeme
            x = 5"""
    fixer.check(b, a)


def test_3(fixer):
    b = """
        def foo(((a, b), c), d) -> e:
            x = 5"""

    a = """
        def foo(xxx_todo_changeme, d) -> e:
            ((a, b), c) = xxx_todo_changeme
            x = 5"""
    fixer.check(b, a)


def test_semicolon(fixer):
    b = """
        def foo(((a, b), c)): x = 5; y = 7"""

    a = """
        def foo(xxx_todo_changeme): ((a, b), c) = xxx_todo_changeme; x = 5; y = 7"""
    fixer.check(b, a)


def test_keywords(fixer):
    b = """
        def foo(((a, b), c), d, e=5) -> z:
            x = 5"""

    a = """
        def foo(xxx_todo_changeme, d, e=5) -> z:
            ((a, b), c) = xxx_todo_changeme
            x = 5"""
    fixer.check(b, a)


def test_varargs(fixer):
    b = """
        def foo(((a, b), c), d, *vargs, **kwargs) -> z:
            x = 5"""

    a = """
        def foo(xxx_todo_changeme, d, *vargs, **kwargs) -> z:
            ((a, b), c) = xxx_todo_changeme
            x = 5"""
    fixer.check(b, a)


def test_multi_1(fixer):
    b = """
        def foo(((a, b), c), (d, e, f)) -> z:
            x = 5"""

    a = """
        def foo(xxx_todo_changeme, xxx_todo_changeme1) -> z:
            ((a, b), c) = xxx_todo_changeme
            (d, e, f) = xxx_todo_changeme1
            x = 5"""
    fixer.check(b, a)


def test_multi_2(fixer):
    b = """
        def foo(x, ((a, b), c), d, (e, f, g), y) -> z:
            x = 5"""

    a = """
        def foo(x, xxx_todo_changeme, d, xxx_todo_changeme1, y) -> z:
            ((a, b), c) = xxx_todo_changeme
            (e, f, g) = xxx_todo_changeme1
            x = 5"""
    fixer.check(b, a)


def test_docstring(fixer):
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
    fixer.check(b, a)


def test_lambda_no_change(fixer):
    s = """lambda x: x + 5"""
    fixer.unchanged(s)


def test_lambda_parens_single_arg(fixer):
    b = """lambda (x): x + 5"""
    a = """lambda x: x + 5"""
    fixer.check(b, a)

    b = """lambda(x): x + 5"""
    a = """lambda x: x + 5"""
    fixer.check(b, a)

    b = """lambda ((((x)))): x + 5"""
    a = """lambda x: x + 5"""
    fixer.check(b, a)

    b = """lambda((((x)))): x + 5"""
    a = """lambda x: x + 5"""
    fixer.check(b, a)


def test_lambda_simple(fixer):
    b = """lambda (x, y): x + f(y)"""
    a = """lambda x_y: x_y[0] + f(x_y[1])"""
    fixer.check(b, a)

    b = """lambda(x, y): x + f(y)"""
    a = """lambda x_y: x_y[0] + f(x_y[1])"""
    fixer.check(b, a)

    b = """lambda (((x, y))): x + f(y)"""
    a = """lambda x_y: x_y[0] + f(x_y[1])"""
    fixer.check(b, a)

    b = """lambda(((x, y))): x + f(y)"""
    a = """lambda x_y: x_y[0] + f(x_y[1])"""
    fixer.check(b, a)


def test_lambda_one_tuple(fixer):
    b = """lambda (x,): x + f(x)"""
    a = """lambda x1: x1[0] + f(x1[0])"""
    fixer.check(b, a)

    b = """lambda (((x,))): x + f(x)"""
    a = """lambda x1: x1[0] + f(x1[0])"""
    fixer.check(b, a)


def test_lambda_simple_multi_use(fixer):
    b = """lambda (x, y): x + x + f(x) + x"""
    a = """lambda x_y: x_y[0] + x_y[0] + f(x_y[0]) + x_y[0]"""
    fixer.check(b, a)


def test_lambda_simple_reverse(fixer):
    b = """lambda (x, y): y + x"""
    a = """lambda x_y: x_y[1] + x_y[0]"""
    fixer.check(b, a)


def test_lambda_nested(fixer):
    b = """lambda (x, (y, z)): x + y + z"""
    a = """lambda x_y_z: x_y_z[0] + x_y_z[1][0] + x_y_z[1][1]"""
    fixer.check(b, a)

    b = """lambda (((x, (y, z)))): x + y + z"""
    a = """lambda x_y_z: x_y_z[0] + x_y_z[1][0] + x_y_z[1][1]"""
    fixer.check(b, a)


def test_lambda_nested_multi_use(fixer):
    b = """lambda (x, (y, z)): x + y + f(y)"""
    a = """lambda x_y_z: x_y_z[0] + x_y_z[1][0] + f(x_y_z[1][0])"""
    fixer.check(b, a)
