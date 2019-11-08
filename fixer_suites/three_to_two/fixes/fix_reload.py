"""Fixer for reload().

importlib.reload(s) -> reload(s)"""

# Local imports
from crosswind import fixer_base
from crosswind.fixer_util import BlankLine, Name, Node, syms


class FixReload(fixer_base.BaseFix):
    BM_compatible = True
    order = "pre"

    PATTERN = """
    power< 'importlib' trailer< '.' 'reload' > args=any* > |
    import_name< 'import' 'importlib' >
    """

    def transform(self, node, results):
        arg_list = results.get("args")

        if node.type == syms.import_name:
            new = BlankLine()
            return new

        elif arg_list:
            args = arg_list[0]
            args = args.clone()
            prefix = node.prefix
            return Node(syms.power, [Name("reload"), args], prefix=prefix)
