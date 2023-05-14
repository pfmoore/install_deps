import os
import subprocess
from textwrap import dedent

import pytest

import install_deps


def test_arg_parsing():
    args = install_deps.parse_args(["something"])
    assert args.filename == "something"


def test_pip_invocation(tmp_path, monkeypatch):
    pyproject = dedent(
        """
    [project]
    name = "test"
    version = "0.1"
    dependencies = ["foo", "bar"]
    """
    )

    pyproject_file = tmp_path / "pyproject.toml"
    pyproject_file.write_text(pyproject, encoding="utf-8")

    def run_tester(*args, **kw):
        assert args[0][1:] == ["-m", "pip", "install", "foo", "bar"]

    monkeypatch.setattr(subprocess, "run", run_tester)
    install_deps.install_deps_from(os.fspath(pyproject_file))


def test_no_metadata(tmp_path, monkeypatch):
    pyproject = dedent(
        """
    name = "test"
    version = "0.1"
    """
    )

    pyproject_file = tmp_path / "pyproject.toml"
    pyproject_file.write_text(pyproject, encoding="utf-8")

    def run_fail(*args, **kw):
        assert False, "We should not run pip here"

    monkeypatch.setattr(subprocess, "run", run_fail)
    with pytest.raises(ValueError, match="No PEP 621 metadata.*"):
        install_deps.install_deps_from(os.fspath(pyproject_file))


def test_no_dependencies(tmp_path, monkeypatch, capsys):
    pyproject = dedent(
        """
    [project]
    name = "test"
    version = "0.1"
    """
    )

    pyproject_file = tmp_path / "pyproject.toml"
    pyproject_file.write_text(pyproject, encoding="utf-8")

    def run_fail(*args, **kw):
        assert False, "We should not run pip here"

    monkeypatch.setattr(subprocess, "run", run_fail)
    install_deps.install_deps_from(os.fspath(pyproject_file))
    cap = capsys.readouterr()
    assert cap.out.startswith("No dependencies specified")


def test_dynamic_dependencies(tmp_path, monkeypatch):
    pyproject = dedent(
        """
    [project]
    name = "test"
    version = "0.1"
    dynamic = ["dependencies"]
    dependencies = ["foo", "bar"]
    """
    )

    pyproject_file = tmp_path / "pyproject.toml"
    pyproject_file.write_text(pyproject, encoding="utf-8")

    def run_fail(*args, **kw):
        assert False, "We should not run pip here"

    monkeypatch.setattr(subprocess, "run", run_fail)
    with pytest.raises(ValueError, match=".*cannot be dynamic"):
        install_deps.install_deps_from(os.fspath(pyproject_file))
