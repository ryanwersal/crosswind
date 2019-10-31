import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(three_to_two_test_case):
    return three_to_two_test_case("collections")


def test_from_UserDict(fixer):

    b = """
    from collections import UserDict"""
    a = """
    from UserDict import UserDict"""
    fixer.check(b, a)


def test_from_UserList(fixer):

    b = """
    from collections import UserList"""
    a = """
    from UserList import UserList"""
    fixer.check(b, a)


def test_from_UserString(fixer):

    b = """
    from collections import UserString"""
    a = """
    from UserString import UserString"""
    fixer.check(b, a)


def test_using_UserDict(fixer):

    b = """
    class Scapegoat(collections.UserDict):
        pass"""
    a = """import UserDict

class Scapegoat(UserDict.UserDict):
    pass"""
    fixer.check(b, a)


def test_using_UserList(fixer):

    b = """
    class Scapegoat(collections.UserList):
        pass"""
    a = """import UserList

class Scapegoat(UserList.UserList):
    pass"""
    fixer.check(b, a)


def test_using_UserString(fixer):

    b = """
    class Scapegoat(collections.UserString):
        pass"""
    a = """import UserString

class Scapegoat(UserString.UserString):
    pass"""
    fixer.check(b, a)
