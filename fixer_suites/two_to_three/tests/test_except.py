import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(two_to_three_test_case):
    return two_to_three_test_case("except")


def test_prefix_preservation(fixer):
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
    fixer.check(b, a)


def test_simple(fixer):
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
    fixer.check(b, a)


def test_simple_no_space_before_target(fixer):
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
    fixer.check(b, a)


def test_tuple_unpack(fixer):
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
    fixer.check(b, a)


def test_multi_class(fixer):
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
    fixer.check(b, a)


def test_list_unpack(fixer):
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
    fixer.check(b, a)


def test_weird_target_1(fixer):
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
    fixer.check(b, a)


def test_weird_target_2(fixer):
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
    fixer.check(b, a)


def test_weird_target_3(fixer):
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
    fixer.check(b, a)


def test_bare_except(fixer):
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
    fixer.check(b, a)


def test_bare_except_and_else_finally(fixer):
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
    fixer.check(b, a)


def test_multi_fixed_excepts_before_bare_except(fixer):
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
    fixer.check(b, a)


def test_one_line_suites(fixer):
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
    fixer.check(b, a)
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
    fixer.check(b, a)
    b = """
        try: raise TypeError
        except TypeError, e: pass
        """
    a = """
        try: raise TypeError
        except TypeError as e: pass
        """
    fixer.check(b, a)
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
    fixer.check(b, a)


# These should not be touched:


def test_unchanged_1(fixer):
    s = """
        try:
            pass
        except:
            pass"""
    fixer.unchanged(s)


def test_unchanged_2(fixer):
    s = """
        try:
            pass
        except Exception:
            pass"""
    fixer.unchanged(s)


def test_unchanged_3(fixer):
    s = """
        try:
            pass
        except (Exception, SystemExit):
            pass"""
    fixer.unchanged(s)
