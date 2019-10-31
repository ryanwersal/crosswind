def test_bit_length_support_int():
    """Confirm that bit_length is indeed supported on 2.7."""
    v = 15
    assert v.bit_length() == (len(bin(v)) - 2)

def test_bit_length_support_long():
    """Confirm long behaviors as well."""
    v = 15L
    assert v.bit_length() == (len(bin(v)) - 2)
