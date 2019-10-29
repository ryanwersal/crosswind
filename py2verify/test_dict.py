def test_confirm_key_in_dict_supported():
    """Confirms that `k in d` syntax supported."""
    assert "foo" in {"foo": "bar"}
