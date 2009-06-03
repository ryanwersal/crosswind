"""Fix bound method attributes (method.im_? -> method.__?__).
"""

# Local imports
from lib2to3 import fixer_base
from lib2to3.fixer_util import Name

MAP = {
    "__func__" : "im_func",
    "__self__" : "im_self"
    # Fortunately, im_self.__class__ == im_class in 2.5.
    }

class FixMethodattrs(fixer_base.BaseFix):
    PATTERN = """
    power< any+ trailer< '.' attr=('__func__' | '__self__') > any* >
    """

    def transform(self, node, results):
        attr = results["attr"][0]
        new = unicode(MAP[attr.value])
        attr.replace(Name(new, prefix=attr.prefix))
