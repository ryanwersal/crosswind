def test_repr_works_as_expected():
    """Confirm repr call works same as literal syntax."""
    x = {"foo": "bar"}
    assert `x` == repr(x)
