import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(three_to_two_test_case):
    return three_to_two_test_case("getcwd")


def test_prefix_preservation(fixer):
    b = """ls =    os.listdir(  os.getcwd()  )"""
    a = """ls =    os.listdir(  os.getcwdu()  )"""
    fixer.check(b, a)

    b = """whatdir = os.getcwd      (      )"""
    a = """whatdir = os.getcwdu      (      )"""
    fixer.check(b, a)
