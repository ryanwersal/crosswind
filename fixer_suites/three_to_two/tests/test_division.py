from .support import crosswindFixerTestCase
from itertools import count


class Test_division(crosswindFixerTestCase):
    fixer = "division"

    counter = count(1)
    divisions = [
        ("1", "2"),
        ("spam", "eggs"),
        ("lambda a: a(4)", "my_foot(your_face)"),
        ("temp(bob)", "4"),
        ("29.4", "green()"),
    ]

    for top, bottom in divisions:
        exec(
            'def test_%d(self):\n    b = "%s/%s"\n    a = "from __future__ import division\\n%s/%s"\n    self.check(b, a)'
            % (next(counter), top, bottom, top, bottom)
        )
