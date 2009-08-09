from test_all_fixers import lib3to2FixerTestCase

class Test_imports2(lib3to2FixerTestCase):
    fixer = "imports2"
    
    def test_imports(self):
    
        b = "from urllib.request import urlopen"
        a = "from urllib2 import urlopen"
        self.check(b, a)
        
        b = "from urllib.request import urlopen\n"\
        "from urllib.parse import urlencode"
        a = "from urllib2 import urlopen\n"\
        "from urllib import urlencode"
        self.check(b, a)
        
        b = "from tkinter.simpledialog import Grid, SimpleDialog"
        a = "from tkSimpleDialog import Grid\n"\
        "from SimpleDialog import SimpleDialog"
        self.check(b, a)
