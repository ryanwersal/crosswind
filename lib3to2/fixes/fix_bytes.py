"""
Fixer for bytes -> str.
"""

import re
from lib2to3 import fixer_base
from ..fixer_util import Name, token, parse_args, Call, Comma

_literal_re = re.compile(r"[bB][rR]?[\'\"]")

class FixBytes(fixer_base.BaseFix):

    PATTERN = "STRING | power< name='bytes' trailer< '(' (args=arglist | any*) ')' > >"

    def match(self, node):
        results = super().match(node)
        if not results:
            if node.type == token.NAME and node.value == "bytes":
                return {"node": node, "name": node}
        return results

    def transform(self, node, results):
        new = node.clone()
        name = results.get("name")
        arglist = results.get("args")
        if name is not None:
            assert name.value == "bytes"
            name.replace(Name("str", prefix=name.prefix))
        elif node.type == token.STRING:
            if _literal_re.match(node.value):
                new.value = new.value[1:]
                return new
        if arglist is not None:
            args = arglist.children
            source, encoding, errors = parse_args(args, ("source", "encoding", "errors"))

            encoding.prefix = ""
            if errors is None:
                arglist.replace(Call(Name(source.value + ".encode"), (encoding,)))
            else:
                errors.prefix = " "
                arglist.replace(Call(Name(source.value + ".encode"), (encoding, Comma(), errors)))
