import os
import tempfile


def test_open_without_import():
    """Confirm using open without importing from io works in Python 2.7."""
    temp_file_handle, temp_path = tempfile.mkstemp(suffix='txt', prefix='')
    os.close(temp_file_handle)

    with open(temp_path, "w") as test_file:
        test_file.write(u"Test.")

    os.remove(temp_path)

def test_open_with_import():
    """Confirm using open imported from io works in Python 2.7."""
    from io import open
    temp_file_handle, temp_path = tempfile.mkstemp(suffix='txt', prefix='')
    os.close(temp_file_handle)

    with open(temp_path, "w") as test_file:
        test_file.write(u"Test with import.")

    os.remove(temp_path)
