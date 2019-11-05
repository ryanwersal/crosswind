import os


def test_open_without_import(tmpdir):
    """Confirm using open without importing from io works in Python 2.7."""
    tmp_file_path = os.path.join(str(tmpdir), "test.txt")

    with open(tmp_file_path, "w") as test_file:
        test_file.write(u"Test.")

def test_open_with_import(tmpdir):
    """Confirm using open imported from io works in Python 2.7."""
    from io import open
    tmp_file_path = os.path.join(str(tmpdir), "test.txt")

    with open(tmp_file_path, "w") as test_file:
        test_file.write(u"Test with import.")
