"""
Fixer for Python 3 function parameter syntax
"""

from lib2to3 import fixer_base
from ..fixer_util import token

def needs_fixing(after_star):
    """
    Returns string with the name of the kwargs dict if the args after the first star need fixing
    Otherwise returns empty string
    """
    if after_star[0].type == token.STAR:
        return ''
    found_kwargs = False
    needs_fix = False

    for t in after_star[1:]:
        if t.type == token.COMMA:
            # Commas are irrelevant at this stage.
            continue
        elif t.type == token.NAME and not found_kwargs:
            # Keyword-only argument: definitely need to fix.
            needs_fix = True
        elif t.type == token.NAME and found_kwargs:
            # Return 'foobar' of **foobar, if needed.
            return t.value if needs_fix else ''
        elif t.type == token.STAR:
            # Found either '*' from **foobar.
            found_kwargs = True
    else:
        # Never found **foobar.  Return a synthetic name, if needed.
        return '_3to2kwargs' if needs_fix else ''

class FixKwargs(fixer_base.BaseFix):

    explicit = True # not sufficiently tested
    
    PATTERN = "funcdef< 'def' NAME parameters< '(' typedargslist< any* first_star='*' after_star=any* > ')' > ':' suite=any >"

    def transform(self, node, results):
        after_star = results["after_star"]
        new_kwargs = needs_fixing(after_star)
        if not new_kwargs:
            return
        else:
            print("Placeholder!")
