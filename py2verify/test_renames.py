import sys


def test_maxint_maxsize_interchangable():
    """Confirm that sys.maxint and sys.maxsize are interchangable."""
    assert sys.maxint == sys.maxsize
