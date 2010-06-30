"""
Fixer for:
collections.UserDict -> UserDict.UserDict
collections.UserList -> UserList.UserList
collections.UserString -> UserString.UserString
"""

from lib2to3 import fixer_base

class FixCollections(fixer_base.BaseFix):

    explicit = True

    def match(self, node):
        return False

    def transform(self, node, results):

        pass # stub
