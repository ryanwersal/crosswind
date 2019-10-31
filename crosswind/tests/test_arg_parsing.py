import os

import pytest

from crosswind import main


@pytest.fixture
def toml_config(tmpdir):
    """
    Writes TOML configuration for use in configuration tests.
    """
    toml_path = os.path.join(tmpdir, "pyproject.toml")
    with open(toml_path, "w") as toml:
        toml.write(
            """
        [tool.crosswind.preset.foo]
        [tool.crosswind.preset.bar]
        """
        )
    yield toml_path


def test_handles_no_toml_file():
    main.main([])


def test_toml_can_list_available_presets(toml_config, capsys):
    main.main(["--list-presets", "--config-file", toml_config])

    captured = capsys.readouterr()
    assert "foo" in captured.out
    assert "bar" in captured.out
