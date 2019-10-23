from .support import crosswindFixerTestCase


class Test_fullargspec(crosswindFixerTestCase):

    fixer = "fullargspec"

    def test_import(self):
        b = "from inspect import blah, blah, getfullargspec, blah, blah"
        a = "from inspect import blah, blah, getargspec, blah, blah"
        self.warns(
            b, a, "some of the values returned by getfullargspec are not valid in Python 2 and have no equivalent."
        )

    def test_usage(self):
        b = "argspec = inspect.getfullargspec(func)"
        a = "argspec = inspect.getargspec(func)"
        self.warns(
            b, a, "some of the values returned by getfullargspec are not valid in Python 2 and have no equivalent."
        )
