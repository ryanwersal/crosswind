from itertools import imap


def test_can_use_imap_only_with_import():
    """Confirms that an itertools import is required for imap."""
    assert list(imap(pow, [2, 3, 10], [5, 2, 3])) == [32, 9, 1000]
