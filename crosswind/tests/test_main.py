# -*- coding: utf-8 -*-
import codecs
import io
import logging
import os
import re
import shutil
import sys
import tempfile

import pytest

from crosswind import main


TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
PY2_TEST_MODULE = os.path.join(TEST_DATA_DIR, "py2_test_grammar.py")


class SampleSource:
    def __init__(self, temp_dir):
        self.py2_src_dir = os.path.join(temp_dir, "python2_project")
        self.py3_dest_dir = os.path.join(temp_dir, "python3_project")

        os.mkdir(self.py2_src_dir)
        os.mkdir(self.py3_dest_dir)

        # Turn it into a package with a few files.
        self.setup_files = []
        open(os.path.join(self.py2_src_dir, "__init__.py"), "w").close()
        self.setup_files.append("__init__.py")
        shutil.copy(PY2_TEST_MODULE, self.py2_src_dir)
        self.setup_files.append(os.path.basename(PY2_TEST_MODULE))
        self.trivial_py2_file = os.path.join(self.py2_src_dir, "trivial.py")
        self.init_py2_file = os.path.join(self.py2_src_dir, "__init__.py")
        with open(self.trivial_py2_file, "w") as trivial:
            trivial.write("print 'I need a simple conversion.'")
        self.setup_files.append("trivial.py")


@pytest.fixture
def sample_source(tmpdir):
    """
    Fixture to manage temp directory, creation of sample conversion files, and cleaning up logging.
    """
    yield SampleSource(tmpdir)
    # Clean up logging configuration down by main.
    del logging.root.handlers[:]


def run_2to3_capture(args):
    args.extend(["--fixer-suites", "fixer_suites.two_to_three"])
    return main.main(args)


def test_unencodable_diff(monkeypatch, capsys):
    input_stream = io.StringIO("print 'nothing'\nprint u'über'\n")
    monkeypatch.setattr("sys.stdin", input_stream)

    out = io.BytesIO()
    output_stream = codecs.getwriter("ascii")(out)
    monkeypatch.setattr("sys.stdout", output_stream)

    ret = run_2to3_capture(["-"])
    assert ret == 0

    assert "-print 'nothing'" in out.getvalue().decode("ascii")

    captured = capsys.readouterr()
    assert "WARNING: couldn't encode <stdin>'s diff for your terminal" in captured.err


def test_filename_changing_on_output_single_dir(sample_source, capsys, caplog):
    """2to3 a single directory with a new output dir and suffix."""
    caplog.set_level(logging.INFO)

    suffix = "TEST"
    ret = run_2to3_capture(
        [
            "-n",
            "--add-suffix",
            suffix,
            "--write-unchanged-files",
            "--no-diffs",
            "--output-dir",
            sample_source.py3_dest_dir,
            sample_source.py2_src_dir,
        ]
    )
    assert ret == 0

    captured = capsys.readouterr()
    assert "implies -w." in captured.err

    assert (
        f"Output in {sample_source.py3_dest_dir!r} will mirror the input directory {sample_source.py2_src_dir!r} layout"
        in caplog.text
    )

    assert set(name + suffix for name in sample_source.setup_files) == set(os.listdir(sample_source.py3_dest_dir))
    for name in sample_source.setup_files:
        py2_path = os.path.join(sample_source.py2_src_dir, name)
        py3_path = os.path.join(sample_source.py3_dest_dir, name + suffix)
        assert f"Writing converted {py2_path} to {py3_path}" in caplog.text

    assert re.search(r"No changes to .*__init__\.py", caplog.text) is not None


def test_filename_changing_on_output_two_files(sample_source, caplog):
    """2to3 two files in one directory with a new output dir."""
    caplog.set_level(logging.INFO)

    py2_files = [sample_source.trivial_py2_file, sample_source.init_py2_file]
    expected_files = set(os.path.basename(name) for name in py2_files)
    ret = run_2to3_capture(
        ["-n", "-w", "--write-unchanged-files", "--no-diffs", "--output-dir", sample_source.py3_dest_dir] + py2_files
    )
    assert ret == 0

    assert (
        f"Output in {sample_source.py3_dest_dir!r} will mirror the input directory {sample_source.py2_src_dir!r} layout"
        in caplog.text
    )
    assert expected_files == set(os.listdir(sample_source.py3_dest_dir))


def test_filename_changing_on_output_single_file(sample_source, caplog):
    """2to3 a single file with a new output dir."""
    caplog.set_level(logging.INFO)

    ret = run_2to3_capture(
        ["-n", "-w", "--no-diffs", "--output-dir", sample_source.py3_dest_dir, sample_source.trivial_py2_file]
    )
    assert ret == 0

    assert (
        f"Output in {sample_source.py3_dest_dir!r} will mirror the input directory {sample_source.py2_src_dir!r} layout"
        in caplog.text
    )
    assert set([os.path.basename(sample_source.trivial_py2_file)]) == set(os.listdir(sample_source.py3_dest_dir))
