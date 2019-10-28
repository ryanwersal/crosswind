def test_chr_works():
	"""Confirms that chr works in Py2.7 so no reason to have three_to_fix fix it."""
	assert chr(97) == unichr(97)
