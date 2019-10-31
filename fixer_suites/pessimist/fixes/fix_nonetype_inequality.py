"""
Fixer for inequality comparison with a variable.

In Python 2 None was treated as less than any number. Pessimistically we should
enter the conditional block if the variable is None.
`if foo < 5:` -> `if foo is None or foo < 5:`

The greater than case is less unfortunate since we should _not_ enter the conditional
body.
`if foo > 5:` -> `if foo is not None and foo > 5:`
"""

from operator import itemgetter

from crosswind import fixer_base
from crosswind.fixer_util import AndTest, Comparison, CompositeOperator, NoneValue, Operator, OrTest
from crosswind.pgen2 import token
from crosswind.pygram import python_symbols as syms


class FixNonetypeInequality(fixer_base.BaseFix):

    PATTERN = "if_stmt< 'if' comparison=comparison< left=any operator=any right=any > ':' any* >"

    def transform(self, node, results):
        assert "comparison" in results
        assert "left" in results
        assert "operator" in results
        assert "right" in results

        comparison, left, operator, right = itemgetter("comparison", "left", "operator", "right")(results)

        # If operator is a composite operator we don't need to proceed as we only care about inequality cases.
        if operator.type == syms.comp_op:
            return

        if left.type == token.NAME:
            if operator.value in ("<", "<="):
                none_comparison = Comparison(left.clone(), Operator("is", prefix=" "), NoneValue(prefix=" "))
                comparison.replace(OrTest(none_comparison, comparison.clone()))

            elif operator.value in (">", ">="):
                operator = CompositeOperator(Operator("is", prefix=" "), Operator("not", prefix=" "))
                none_comparison = Comparison(left.clone(), operator, NoneValue(prefix=" "))
                comparison.replace(AndTest(none_comparison, comparison.clone()))

        elif right.type == token.NAME:
            if operator.value in ("<", "<="):
                operator = CompositeOperator(Operator("is", prefix=" "), Operator("not", prefix=" "))
                none_comparison = Comparison(right.clone(), operator, NoneValue(prefix=" "))
                comparison.replace(AndTest(none_comparison, comparison.clone()))

            elif operator.value in (">", ">="):
                none_comparison = Comparison(right.clone(), Operator("is", prefix=" "), NoneValue(prefix=" "))
                comparison.replace(OrTest(none_comparison, comparison.clone()))
