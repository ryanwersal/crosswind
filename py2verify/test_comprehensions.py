def test_list_comprehension_okay_with_no_parens():
    """Confirms list comprehensions with in clauses lacking parens are okay in 2.7."""
    assert [x for x in 1, 2] == [1, 2]

def test_list_comprehension_okay_with_parens():
    """Confirms that list comprehensions with parens are okay as well. Allows skipping 3to2 stripping such parens."""
    assert [x for x in (1, 2)] == [1, 2]
