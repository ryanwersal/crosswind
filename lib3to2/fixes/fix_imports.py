"""Fix renamed imports and module references."""

import re

from lib2to3.fixes.fix_imports import FixImports as FixImports_

MAPPING = {'winreg': '_winreg',
           'configparser': 'ConfigParser',
           'copyreg': 'copy_reg',
           'queue': 'Queue',
           'socketserver': 'SocketServer',
           '_markupbase': 'markupbase',
           'test.support': 'test.test_support',
           'dbm.bsd': 'dbhash',
           'dbm.ndbm': 'dbm',
           'dbm.dumb': 'dumbdbm',
           'dbm.gnu': 'gdbm',
           'html.parser': 'HTMLParser',
           'html.entities': 'htmlentitydefs',
           'http.client': 'httplib',
           'http.cookies': 'Cookie',
           'http.cookiejar': 'cookielib',
           'tkinter.dialog': 'Dialog',
           'tkinter._fix': 'FixTk',
           'tkinter.scrolledtext': 'ScrolledText',
           'tkinter.tix': 'Tix',
           'tkinter.constants': 'Tkconstants',
           'tkinter.dnd': 'Tkdnd',
           'tkinter.__init__': 'Tkinter',
           'tkinter.colorchooser': 'tkColorChooser',
           'tkinter.commondialog': 'tkCommonDialog',
           'tkinter.font': 'tkFont',
           'tkinter.messagebox': 'tkMessageBox',
           'tkinter.turtle': 'turtle',
           'urllib.robotparser': 'robotparser',
           'xmlrpc.client': 'xmlrpclib',
}

class FixImports(FixImports_):

    mapping = MAPPING

    # This function is just not ready to be included yet.
    # It needs to return a results mapping, but right now it only functions to
    # match dotted import names from the mapping.
    
    #TODO: Make this work right

    def match_dotted(self, node):
        """Iterate through names trying to match dotted ones"""
        for name in self.mapping.keys():
            if '.' in name:
                if name in str(node):
                    assert re.match("import *" + name , str(node))
                    #This next line needs to return a proper results dict
                    return {'node': node}

    def match(self, node):
        #XXX Uncomment the second part of the next line when match_dotted works
        return super(FixImports, self).match(node) #or match_dotted(node)
