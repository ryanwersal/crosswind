from crosswind.tests.support import FixerTestCase


class Test_except(FixerTestCase):
    fixer = "except"

    def test_prefix_preservation(self):
        b = """
            try:
                pass
            except (RuntimeError, ImportError),    e:
                pass"""
        a = """
            try:
                pass
            except (RuntimeError, ImportError) as    e:
                pass"""
        self.check(b, a)

    def test_simple(self):
        b = """
            try:
                pass
            except Foo, e:
                pass"""
        a = """
            try:
                pass
            except Foo as e:
                pass"""
        self.check(b, a)

    def test_simple_no_space_before_target(self):
        b = """
            try:
                pass
            except Foo,e:
                pass"""
        a = """
            try:
                pass
            except Foo as e:
                pass"""
        self.check(b, a)

    def test_tuple_unpack(self):
        b = """
            def foo():
                try:
                    pass
                except Exception, (f, e):
                    pass
                except ImportError, e:
                    pass"""

        a = """
            def foo():
                try:
                    pass
                except Exception as xxx_todo_changeme:
                    (f, e) = xxx_todo_changeme.args
                    pass
                except ImportError as e:
                    pass"""
        self.check(b, a)

    def test_multi_class(self):
        b = """
            try:
                pass
            except (RuntimeError, ImportError), e:
                pass"""

        a = """
            try:
                pass
            except (RuntimeError, ImportError) as e:
                pass"""
        self.check(b, a)

    def test_list_unpack(self):
        b = """
            try:
                pass
            except Exception, [a, b]:
                pass"""

        a = """
            try:
                pass
            except Exception as xxx_todo_changeme:
                [a, b] = xxx_todo_changeme.args
                pass"""
        self.check(b, a)

    def test_weird_target_1(self):
        b = """
            try:
                pass
            except Exception, d[5]:
                pass"""

        a = """
            try:
                pass
            except Exception as xxx_todo_changeme:
                d[5] = xxx_todo_changeme
                pass"""
        self.check(b, a)

    def test_weird_target_2(self):
        b = """
            try:
                pass
            except Exception, a.foo:
                pass"""

        a = """
            try:
                pass
            except Exception as xxx_todo_changeme:
                a.foo = xxx_todo_changeme
                pass"""
        self.check(b, a)

    def test_weird_target_3(self):
        b = """
            try:
                pass
            except Exception, a().foo:
                pass"""

        a = """
            try:
                pass
            except Exception as xxx_todo_changeme:
                a().foo = xxx_todo_changeme
                pass"""
        self.check(b, a)

    def test_bare_except(self):
        b = """
            try:
                pass
            except Exception, a:
                pass
            except:
                pass"""

        a = """
            try:
                pass
            except Exception as a:
                pass
            except:
                pass"""
        self.check(b, a)

    def test_bare_except_and_else_finally(self):
        b = """
            try:
                pass
            except Exception, a:
                pass
            except:
                pass
            else:
                pass
            finally:
                pass"""

        a = """
            try:
                pass
            except Exception as a:
                pass
            except:
                pass
            else:
                pass
            finally:
                pass"""
        self.check(b, a)

    def test_multi_fixed_excepts_before_bare_except(self):
        b = """
            try:
                pass
            except TypeError, b:
                pass
            except Exception, a:
                pass
            except:
                pass"""

        a = """
            try:
                pass
            except TypeError as b:
                pass
            except Exception as a:
                pass
            except:
                pass"""
        self.check(b, a)

    def test_one_line_suites(self):
        b = """
            try: raise TypeError
            except TypeError, e:
                pass
            """
        a = """
            try: raise TypeError
            except TypeError as e:
                pass
            """
        self.check(b, a)
        b = """
            try:
                raise TypeError
            except TypeError, e: pass
            """
        a = """
            try:
                raise TypeError
            except TypeError as e: pass
            """
        self.check(b, a)
        b = """
            try: raise TypeError
            except TypeError, e: pass
            """
        a = """
            try: raise TypeError
            except TypeError as e: pass
            """
        self.check(b, a)
        b = """
            try: raise TypeError
            except TypeError, e: pass
            else: function()
            finally: done()
            """
        a = """
            try: raise TypeError
            except TypeError as e: pass
            else: function()
            finally: done()
            """
        self.check(b, a)

    # These should not be touched:

    def test_unchanged_1(self):
        s = """
            try:
                pass
            except:
                pass"""
        self.unchanged(s)

    def test_unchanged_2(self):
        s = """
            try:
                pass
            except Exception:
                pass"""
        self.unchanged(s)

    def test_unchanged_3(self):
        s = """
            try:
                pass
            except (Exception, SystemExit):
                pass"""
        self.unchanged(s)
