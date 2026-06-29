import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_cli_smoke_lunar_scenario(tmp_path):
    scenario = ROOT / "scenarios" / "lunar_base.yaml"
    env = {**os.environ, "PYTHONPATH": str(ROOT / "src")}
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "astrosim.cli",
            str(scenario),
            "--output-dir",
            str(tmp_path),
            "--no-plot",
        ],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert (tmp_path / "lunar_base_alpha.json").exists()
    assert (tmp_path / "lunar_base_alpha.csv").exists()
    assert "Results written to" in result.stdout


def test_cli_monte_carlo_writes_summary(tmp_path):
    scenario = ROOT / "scenarios" / "lunar_base.yaml"
    env = {**os.environ, "PYTHONPATH": str(ROOT / "src")}
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "astrosim.cli",
            str(scenario),
            "--output-dir",
            str(tmp_path),
            "--no-plot",
            "--monte-carlo",
            "3",
            "--seed",
            "7",
        ],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert (tmp_path / "lunar_base_alpha_monte_carlo_summary.json").exists()
    assert "Monte Carlo: 3 runs" in result.stdout


def test_cli_prints_optimization_suggestions(tmp_path):
    scenario = ROOT / "scenarios" / "lunar_base.yaml"
    env = {**os.environ, "PYTHONPATH": str(ROOT / "src")}
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "astrosim.cli",
            str(scenario),
            "--output-dir",
            str(tmp_path),
            "--no-plot",
        ],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "Optimization suggestions:" in result.stdout


def test_cli_validate_writes_report(tmp_path):
    scenario = ROOT / "scenarios" / "greenhouse_lunar.yaml"
    env = {**os.environ, "PYTHONPATH": str(ROOT / "src")}
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "astrosim.cli",
            str(scenario),
            "--output-dir",
            str(tmp_path),
            "--no-plot",
            "--validate",
        ],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert (tmp_path / "validation_report.json").exists()
    assert "Validation:" in result.stdout