import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(two_to_three_test_case):
    return two_to_three_test_case("collections")


def test_from_UserDict(fixer):

    b = """
    from UserDict import UserDict"""
    a = """
    from collections import UserDict"""
    fixer.check(b, a)


def test_from_UserList(fixer):

    b = """
    from UserList import UserList"""
    a = """
    from collections import UserList"""
    fixer.check(b, a)


def test_from_UserString(fixer):

    b = """
    from UserString import UserString"""
    a = """
    from collections import UserString"""
    fixer.check(b, a)


def test_using_UserDict(fixer):

    b = """
    class Scapegoat(UserDict.UserDict):
        pass"""

    a = """import collections

class Scapegoat(collections.UserDict):
    pass"""
    fixer.check(b, a)


def test_using_UserList(fixer):

    b = """
    class Scapegoat(UserList.UserList):
        pass"""

    a = """import collections

class Scapegoat(collections.UserList):
    pass"""
    fixer.check(b, a)


def test_using_UserString(fixer):

    b = """
    class Scapegoat(UserString.UserString):
        pass"""

    a = """import collections

class Scapegoat(collections.UserString):
    pass"""
    fixer.check(b, a)
