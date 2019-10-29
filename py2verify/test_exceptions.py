import sys


def test_exc_info_and_other_functions_same():
    """Confirm exc info can be extracted without using the specific methods."""
    try:
        raise Exception("foobar")
    except Exception as e:
        ex_type, ex_value, ex_traceback = sys.exc_info()
        assert sys.exc_type == ex_type
        assert sys.exc_value == ex_value
        assert sys.exc_traceback == ex_traceback
