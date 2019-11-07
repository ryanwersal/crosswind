from __future__ import division


def test_true_division_with_future():
    """Confirms true division with ints if future is applied."""
    assert (3 / 2) == 1.5

def test_explicit_floor_division_operator_with_future():
    """Confirms that // is available in py2 unconditionally."""
    assert (3 // 2) == 1
