def _add(*args, **kwargs):
    num = 0
    for a in args:
        num += a
    for v in kwargs.values():
        num += v
    return num

def test_apply_works():
    """Confirms that invoking apply works in Python 2.7."""
    assert apply(_add, [1, 2], {"3": 3, "4": 4}) == 10

def test_direct_invocation_works():
    """Confirms that direct invocation works as well."""
    assert (_add)(*[1, 2], **{"3": 3, "4": 4}) == 10
