"""
Fixer for Python 3 function parameter syntax
"""

# Note: "relevant" parameters are parameters following the first STAR in the list.

from lib2to3 import fixer_base
from ..fixer_util import token

_if_template = "if '%(name)s' in %(kwargs)s: %(name)s = %(kwargs)s['%(name)s']"
_else_template = "else: %(name)s = %(default)s"

def needs_fixing(relevant_params):
    """
    Returns string with the name of the kwargs dict if the params after the first star need fixing
    Otherwise returns empty string
    """
    found_kwargs = False
    needs_fix = False

    for t in relevant_params:
        if t.type == token.COMMA:
            # Commas are irrelevant at this stage.
            continue
        elif t.type == token.NAME and not found_kwargs:
            # Keyword-only argument: definitely need to fix.
            needs_fix = True
        elif t.type == token.NAME and found_kwargs:
            # Return 'foobar' of **foobar, if needed.
            return t.value if needs_fix else ''
        elif t.type == token.DOUBLESTAR:
            # Found either '*' from **foobar.
            found_kwargs = True
    else:
        # Never found **foobar.  Return a synthetic name, if needed.
        return '_3to2kwargs' if needs_fix else ''

class FixKwargs(fixer_base.BaseFix):

    explicit = True # not sufficiently tested
    
    PATTERN = "funcdef< 'def' NAME parameters< '(' typedargslist< params=any* > ')' > ':' suite=any >"

    def transform(self, node, results):
        params = results["params"]
        for i, item in enumerate(params):
            if item.type == token.STAR:
                relevant_params = params[i:]
                break
        else:
            return
        # relevant_params is guaranteed to be a list starting with *.
        # if fixing is needed, there will be at least 3 items in this list:
        # [STAR, COMMA, NAME] is the minimum that we need to worry about.
        new_kwargs = needs_fixing(relevant_params)
        # new_kwargs is the name of the kwargs dictionary.
        if not new_kwargs:
            return

        # At this point, relevant_params is guaranteed to be a list
        # beginning with a star that includes at least one keyword-only param
        # e.g., [STAR, NAME, COMMA, NAME, COMMA, DOUBLESTAR, NAME] or
        # [STAR, COMMA, NAME], or [STAR, COMMA, NAME, COMMA, DOUBLESTAR, NAME]

        
