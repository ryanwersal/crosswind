"""
Fixer for:
map -> itertools.imap
filter -> itertools.ifilter
zip -> itertools.izip
itertools.filterfalse -> itertools.ifilterfalse
"""

from lib2to3 import fixer_base
from lib2to3.fixer_util import touch_import, is_probably_builtin

class FixItertools(fixer_base.BaseFix):

    PATTERN = """
              power< names=('map' | 'filter' | 'zip') any*> |
              import_from< 'from' 'itertools' 'import' imports=any > |
              power< 'itertools' trailer< '.' f='filterfalse' any* > > |
              power< f='filterfalse' any* > any*
              """

    def transform(self, node, results):
        syms = self.syms
        imports = results.get("imports")
        f = results.get("f")
        names = results.get("names")
        if imports:
            if imports.type == syms.import_as_name or not imports.children:
                children = [imports]
            else:
                children = imports.children
            for child in children[::2]:
                if child.value == u"filterfalse":
                    node.changed()
                    child.value = u"ifilterfalse"
                    break
        elif names:
            for name in names:
                if is_probably_builtin(name):
                    name.value = u"i" + name.value
                    touch_import(u"itertools", name.value, node)
        elif f:
            node.changed()
            f.value = u"ifilterfalse"
