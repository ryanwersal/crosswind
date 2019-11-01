"""
Fixer for:
UserDict.UserDict -> collections.UserDict
UserList.UserList -> collections.UserList
UserString.UserString -> collections.UserString
"""

from crosswind.fixer_base import BaseFix
from crosswind.fixer_util import Name, syms, touch_import


class FixCollections(BaseFix):

    PATTERN = """
        import_from< 'from' mod=('UserDict' | 'UserList' | 'UserString') 'import' ('UserDict' | 'UserList' | 'UserString') > |
        power< mod=('UserDict' | 'UserList' | 'UserString') trailer< '.' ('UserDict' | 'UserList' | 'UserString') > any* >
    """

    def transform(self, node, results):
        mod = results["mod"][0]
        mod.replace(Name('collections', prefix=mod.prefix))

        if node.type == syms.power:
            touch_import(None, 'collections', node)
