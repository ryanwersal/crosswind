def test_default_py2_floor_division():
    """Confirms default py2 behavior of floor division with ints."""
    assert (3 / 2) == 1

def test_explicit_floor_division_operator():
    """Confirms that // is available in py2 unconditionally."""
    assert (3 // 2) == 1
