import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(three_to_two_test_case):
    return three_to_two_test_case("setliteral")


def test_unchanged_dict(fixer):
    s = """{"ghoul": 100, "zombie": 50, "gremlin": 40}"""
    fixer.unchanged(s)

    s = """{1: "spider", 2: "hills", 3: "bologna", None: "tapeworm"}"""
    fixer.unchanged(s)

    s = """{}"""
    fixer.unchanged(s)

    s = """{'a':'b'}"""
    fixer.unchanged(s)


def test_simple_literal(fixer):
    b = """{'Rm 101'}"""
    a = """set(['Rm 101'])"""
    fixer.check(b, a)


def test_multiple_items(fixer):
    b = """{'Rm 101',   'Rm 102',  spam,    ham,      eggs}"""
    a = """set(['Rm 101',   'Rm 102',  spam,    ham,      eggs])"""
    fixer.check(b, a)

    b = """{ a,  b,   c,    d,     e}"""
    a = """set([ a,  b,   c,    d,     e])"""
    fixer.check(b, a)


def test_simple_set_comprehension(fixer):
    b = """{x for x in range(256)}"""
    a = """set([x for x in range(256)])"""
    fixer.check(b, a)


def test_complex_set_comprehension(fixer):
    b = """{F(x) for x in range(256) if x%2}"""
    a = """set([F(x) for x in range(256) if x%2])"""
    fixer.check(b, a)

    b = """{(lambda x: 2000 + x)(x) for x, y in {(5, 400), (6, 600), (7, 900), (8, 1125), (9, 1000)}}"""
    a = """set([(lambda x: 2000 + x)(x) for x, y in set([(5, 400), (6, 600), (7, 900), (8, 1125), (9, 1000)])])"""
    fixer.check(b, a)
