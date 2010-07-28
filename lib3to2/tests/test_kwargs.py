from test_all_fixers import lib3to2FixerTestCase

class Test_kwargs(lib3to2FixerTestCase):
    fixer = 'kwargs'

    def test_basic_unchanged(self):
        s = """
        def spam(ham, eggs):
            funky()"""
        self.unchanged(s)


    def test_args_kwargs_unchanged(self):
        s = """
        def spam(ham, *args, **kwargs):
            funky()"""
        self.unchanged(s)


    def test_args_named_pos(self):
        b = """
        def spam(ham, *args, eggs, monkeys):
            funky()"""
        a = """
        def spam(ham, *args, **_3to2kwargs):
            eggs = _3to2kwargs['eggs']
            monkeys = _3to2kwargs['monkeys']
            funky()"""
        self.check(b, a)


    def test_args_named_pos_catchall(self):
        b = """
        def spam(ham, *args, eggs, monkeys, **stuff):
            funky()"""
        a = """
        def spam(ham, *args, **stuff):
            eggs = stuff['eggs']
            monkeys = stuff['monkeys']
            funky()"""
        self.check(b, a)


    def test_bare_star_named(self):
        b = """
        def spam(ham, *, eggs, monkeys):
            funky()"""
        a = """
        def spam(ham, **_3to2kwargs):
            eggs = _3to2kwargs['eggs']
            monkeys = _3to2kwargs['monkeys']            
            funky()"""
        self.check(b, a)


    def test_bare_star_named_defaults(self):
        b = """
        def spam(ham, *, dinosaurs, eggs=3, monkeys=2):
            funky()"""
        a = """
        def spam(ham, **_3to2kwargs):
            dinosaurs = _3to2kwargs['dinosaurs']
            if 'eggs' in _3to2kwargs: eggs = _3to2kwargs['eggs']
            else: eggs = 3
            if 'monkeys' in _3to2kwargs: monkeys = _3to2kwargs['monkeys']
            else: monkeys = 2
            funky()"""
        self.check(b, a)


    def test_bare_star_named_defaults_catchall(self):
        b = """
        def spam(ham, *, dinosaurs, eggs=3, monkeys=2, **stuff):
            funky()"""
        a = """
        def spam(ham, **stuff):
            dinosaurs = stuff['dinosaurs']
            if 'eggs' in stuff: eggs = stuff['eggs']
            else: eggs = 3
            if 'monkeys' in stuff: monkeys = stuff['monkeys']
            else: monkeys = 2
            funky()"""
        self.check(b, a)
        
