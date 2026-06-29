"""Tests for package version."""

import re
from pathlib import Path

import astrosim


def test_version_matches_pyproject():
    text = Path(__file__).resolve().parent.parent.joinpath("pyproject.toml").read_text()
    match = re.search(r'^version = "([^"]+)"', text, re.M)
    assert match is not None
    assert astrosim.__version__ == match.group(1)


def test_cli_version_flag():
    import pytest

    from astrosim.cli import build_parser

    parser = build_parser()
    actions = {tuple(a.option_strings) for a in parser._actions if a.option_strings}
    assert ("--version",) in actions or ("-V", "--version") in actions
    with pytest.raises(SystemExit) as exc:
        parser.parse_args(["--version"])
    assert exc.value.code == 0