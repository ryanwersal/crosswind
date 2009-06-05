"""Fixer for sys.intern().

sys.intern(s) -> intern(s)"""

# Local imports
from lib2to3 import pytree
from lib2to3 import fixer_base
from lib2to3.fixer_util import Name, BlankLine, find_binding, find_root


class FixIntern(fixer_base.BaseFix):

    PATTERN = """
    power< 'sys' trailer < '.' 'intern' >
           trailer< lpar='('
                    ( not(arglist | argument<any '=' any>) obj=any
                      | obj=arglist<(not argument<any '=' any>) any ','> )
                    rpar=')' >
           after=any*
    >
    |
    power< name='intern'
           trailer< lpar='('
           ( not(arglist | argument<any '=' any>) obj=any
                      | obj=arglist<(not argument<any '=' any>) any ','> )
                    rpar=')' >
           after=any*
    >
    """

    def transform(self, node, results):
        name = results.get("name")
        binding = find_binding(u"intern", find_root(node), u"sys")
        if name and binding:
            #this case is easy :-)
            binding.remove()
            return
        binding = find_binding(u"sys", find_root(node), None)
        assert binding # sanity check
        syms = self.syms
        obj = results["obj"].clone()
        if obj.type == syms.arglist:
            newarglist = obj.clone()
        else:
            newarglist = pytree.Node(syms.arglist, [obj.clone()])
        after = results["after"]
        if after:
            after = [n.clone() for n in after]

        new = pytree.Node(syms.power,
                          [Name(u"intern")] +
                          [pytree.Node(syms.trailer,
                                       [results["lpar"].clone(),
                                        newarglist,
                                        results["rpar"].clone()] + after)])
        new.prefix = node.prefix
        return new
