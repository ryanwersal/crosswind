"""
Fixer to alert the user about features in 3.x that do not exist in 2.5
Any matches here will necessarily constrain the input code to work after refactoring
only in later versions of Python than 2.5.
"""

from lib2to3 import fixer_base
from lib2to3.fixer_util import does_tree_import, is_import

def incompatible_feature(obj, node, feature):
    reason = "The following is not backwards compatible with Python 2.5 and will only run in version %s and up: %s" %(feature.min_ver, feature.name)
    obj.cannot_convert(node, reason)

class Feature(object):

    def __init__(self, name, min_ver):
        self.name = name
        self.min_ver = min_ver

class FixFeatures(fixer_base.BaseFix):

    # Run this as late as possible, after optionally fixed features are taken care of.
    run_order = 9
    #TODO: Make the pattern built generically from a mapping.
    PATTERN = """format=power< STRING trailer< '.' 'format' > trailer< '(' any* ')' > > |
                 bin=power< 'bin' trailer< '(' any* ')' > [any*] > |
                 io=import_name< 'import' ('io' | dotted_as_names< any* 'io' any* >) > |
                 io=import_from< 'from' 'io' 'import' any* > |
                 abc=import_name< 'import' ('abc' | dotted_as_names< any* 'abc' any* >) > |
                 abc=import_from< 'from' 'abc' 'import' any* > |
                 numb=import_from< 'from' 'numbers' 'import' any* > |
                 numb=import_name< 'import' ('numbers' | dotted_as_names< any* 'numbers' any* >) > |
                 mem=power< 'memoryview' trailer< '(' any* ')' > [any*] >
              """
    def handle_imports(self, node):
        #TODO: Make the handler generic.
        found = []
        if does_tree_import(None, 'io', node) or \
           (is_import(node) and ' io ' in str(node)):
            found.append(Feature('io package', '2.6'))
        if does_tree_import(None, 'abc', node) or \
           (is_import(node) and ' abc ' in str(node)):
            found.append(Feature('abc package', '2.6'))
        if does_tree_import(None, 'numbers', node) or \
           (is_import(node) and ' numbers ' in str(node)):
            found.append(Feature('numbers package', '2.6'))
        return found

    def transform(self, node, results):
        #TODO: Make the transformation generic.
        def alert_feature(feature):
            return incompatible_feature(self, node, feature)
        if results.get('bin'):
            alert_feature(Feature('bin function', '2.6'))
        if results.get('mem'):
            alert_feature(Feature('memoryview function', '2.7'))
        io = results.get('io')
        abc = results.get('abc')
        numb = results.get('numb')
        if io or numb or abc:
            for found in self.handle_imports(node):
                alert_feature(found)
