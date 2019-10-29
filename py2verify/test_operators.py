import collections
import operator


def test_callable_operator():
    """Confirm that operator is not required for callable."""
    assert operator.isCallable(test_callable_operator) == callable(test_callable_operator)

def test_is_sequence_type_behavior():
    """Confirms behavior of the isSequenceType function."""
    assert operator.isSequenceType([])
    assert operator.isSequenceType(tuple([]))

def test_sequence_type():
    """Confirm that sequence type can be isinstanced."""
    assert isinstance([], collections.Sequence)
    assert isinstance(tuple([]), collections.Sequence)

def test_sequence_type_equivalence():
    """Confirm whether or not we need to go back to operator calls or not."""
    assert operator.isSequenceType([]) == isinstance([], collections.Sequence)
    assert operator.isSequenceType(tuple([])) == isinstance(tuple([]), collections.Sequence)
