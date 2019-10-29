def test_isinstance_equals():
    """Confirms equals is comparable."""
    x = 5
    assert type(x) == int
    assert isinstance(x, int)

def test_isinstance_is():
    """Confirms type check is keyword equivalent to isinstance."""
    x = 5
    assert type(x) is int
    assert isinstance(x, int)

def test_isinstance_not_equals():
    """Confirms inequality of a type with isinstance."""
    x = "foo"
    assert type(x) != int
    assert not isinstance(x, int)

def test_isinstance_is_not():
    """Confirms is not also works with isinstance."""
    x = "foo"
    assert type(x) is not int
    assert not isinstance(x, int)

def test_sorted_equivalent():
    """Confirms in-place sort to sorted is equivalent."""
    v = sorted([1, 3, 2])
    assert v == [1, 2, 3]
