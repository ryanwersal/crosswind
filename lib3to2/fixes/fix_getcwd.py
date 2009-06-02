"""
Fixer that changes os.getcwd() to os.getcwdu().
Also warns about "from os import getcwd", suggesting the fixable form.
"""

from lib2to3 import fixer_base
from lib2to3.fixer_util import Name

class FixGetcwd(fixer_base.BaseFix):

    PATTERN = """
              power< 'os' trailer< dot='.' name='getcwd' > any* >
              |
              import_from< 'from' 'os' 'import' bad='getcwd' >
              """

    def transform(self, node, results):
        if "name" in results:
            name = results["name"]
            name.replace(Name(u"getcwdu", prefix=name.get_prefix()))
        elif "bad" in results:
            self.cannot_convert(node, "import os, use os.getcwd() instead.")
            return
        else:
            raise ValueError("For some reason, the pattern matcher failed.")
