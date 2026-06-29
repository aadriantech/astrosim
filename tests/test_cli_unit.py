"""Unit tests for CLI helpers (no subprocess)."""

from pathlib import Path

import pytest

from astrosim.cli import build_parser, handle_ask, output_stem, parse_args, run_from_args

ROOT = Path(__file__).resolve().parent.parent


def test_output_stem_normalizes_spaces():
    assert output_stem("Lunar Base Alpha") == "lunar_base_alpha"


def test_parse_args_defaults():
    args = parse_args(["scenarios/lunar_base.yaml"])
    assert args.scenario == Path("scenarios/lunar_base.yaml")
    assert args.output_dir == Path("output")
    assert args.no_plot is False
    assert args.web is False
    assert args.monte_carlo is None
    assert args.seed is None


def test_parse_args_monte_carlo_and_flags():
    args = parse_args(
        [
            "scenarios/mars_habitat.yaml",
            "--output-dir",
            "/tmp/out",
            "--no-plot",
            "--web",
            "--monte-carlo",
            "10",
            "--seed",
            "42",
        ]
    )
    assert args.output_dir == Path("/tmp/out")
    assert args.no_plot is True
    assert args.web is True
    assert args.monte_carlo == 10
    assert args.seed == 42


def test_build_parser_has_scenario_positional():
    parser = build_parser()
    actions = {a.dest for a in parser._actions}
    assert "scenario" in actions
    assert "monte_carlo" in actions


@pytest.mark.parametrize("with_plot", [True, False])
def test_run_from_args_writes_artifacts(tmp_path, with_plot, capsys):
    args = parse_args(
        [
            str(ROOT / "scenarios" / "lunar_base.yaml"),
            "--output-dir",
            str(tmp_path),
        ]
        + ([] if with_plot else ["--no-plot"])
    )
    out = run_from_args(args)
    assert out == tmp_path
    assert (tmp_path / "lunar_base_alpha.json").exists()
    assert (tmp_path / "lunar_base_alpha.csv").exists()
    if with_plot:
        assert (tmp_path / "lunar_base_alpha_dashboard.png").exists()
    captured = capsys.readouterr()
    assert "Results written to" in captured.out


def test_handle_ask_dry_run(capsys):
    handle_ask(ROOT / "scenarios" / "lunar_base.yaml", "increase crew to 8")
    captured = capsys.readouterr()
    assert '"dry_run": true' in captured.out
    assert '"crew_count": 8' in captured.out