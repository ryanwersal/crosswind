def test_list_comprehension_okay_with_no_parens():
    """Confirms list comprehensions with in clauses lacking parens are okay in 2.7."""
    assert [x for x in 1, 2] == [1, 2]

def test_list_comprehension_okay_with_parens():
    """Confirms that list comprehensions with parens are okay as well. Allows skipping 3to2 stripping such parens."""
    assert [x for x in (1, 2)] == [1, 2]

def test_dict_comprehension_literals():
    """Confirms that dict comprehension literals are supported."""
    expected = {"foo": "bar", 17: 12}
    assert {k: v for k, v in expected.iteritems()} == expected

def test_set_comprehension_literals():
    """Confirms that set comprehension literals are supported."""
    initial = [1, 4, 3, 4, 2]
    assert {v for v in initial} == set([1, 2, 3, 4])
