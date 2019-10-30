import sys


def test_none_less_than_any_number():
    """Confirm behavior of None when compared against numbers."""
    assert 5 > None
    assert 0 > None
    assert -sys.maxint > None
    assert sys.maxint > None
