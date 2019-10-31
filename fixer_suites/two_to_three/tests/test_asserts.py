import pytest


@pytest.fixture(name="fixer")
def fixer_fixture(two_to_three_test_case):
    return two_to_three_test_case("asserts")


def test_deprecated_names(fixer):
    tests = [
        ("self.assert_(True)", "self.assertTrue(True)"),
        ("self.assertEquals(2, 2)", "self.assertEqual(2, 2)"),
        ("self.assertNotEquals(2, 3)", "self.assertNotEqual(2, 3)"),
        ("self.assertAlmostEquals(2, 3)", "self.assertAlmostEqual(2, 3)"),
        ("self.assertNotAlmostEquals(2, 8)", "self.assertNotAlmostEqual(2, 8)"),
        ("self.failUnlessEqual(2, 2)", "self.assertEqual(2, 2)"),
        ("self.failIfEqual(2, 3)", "self.assertNotEqual(2, 3)"),
        ("self.failUnlessAlmostEqual(2, 3)", "self.assertAlmostEqual(2, 3)"),
        ("self.failIfAlmostEqual(2, 8)", "self.assertNotAlmostEqual(2, 8)"),
        ("self.failUnless(True)", "self.assertTrue(True)"),
        ("self.failUnlessRaises(foo)", "self.assertRaises(foo)"),
        ("self.failIf(False)", "self.assertFalse(False)"),
    ]
    for b, a in tests:
        fixer.check(b, a)


def test_variants(fixer):
    b = "eq = self.assertEquals"
    a = "eq = self.assertEqual"
    fixer.check(b, a)
    b = 'self.assertEquals(2, 3, msg="fail")'
    a = 'self.assertEqual(2, 3, msg="fail")'
    fixer.check(b, a)
    b = 'self.assertEquals(2, 3, msg="fail") # foo'
    a = 'self.assertEqual(2, 3, msg="fail") # foo'
    fixer.check(b, a)
    b = "self.assertEquals (2, 3)"
    a = "self.assertEqual (2, 3)"
    fixer.check(b, a)
    b = "  self.assertEquals (2, 3)"
    a = "  self.assertEqual (2, 3)"
    fixer.check(b, a)
    b = "with self.failUnlessRaises(Explosion): explode()"
    a = "with self.assertRaises(Explosion): explode()"
    fixer.check(b, a)
    b = "with self.failUnlessRaises(Explosion) as cm: explode()"
    a = "with self.assertRaises(Explosion) as cm: explode()"
    fixer.check(b, a)


def test_unchanged(fixer):
    fixer.unchanged("self.assertEqualsOnSaturday")
    fixer.unchanged("self.assertEqualsOnSaturday(3, 5)")
