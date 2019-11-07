"""Warns about past module usage"""
from crosswind import fixer_base


class FixPast(fixer_base.BaseFix):
    BM_compatible = True

    PATTERN = """
        import_from<
            'from' module=(dotted_name<'past' '.' any>)
            'import' obj=any
        >
    """

    def transform(self, node, results):
        module_name = "".join(n.value for n in results["module"].children)
        obj_name = results["obj"].value
        # FIXME: Is there more we can do here? Are there specific cases we can handle more robustly?
        self.warning(node, f"{obj_name!r} imported from {module_name}")
        return None
