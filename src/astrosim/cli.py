"""Command-line interface."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from astrosim.ai.hooks import AIHooks, InsightRequest
from astrosim.engine.monte_carlo import MonteCarloRunner
from astrosim.export.formats import export_csv, export_json
from astrosim.scenario import build_simulator, load_and_build, load_scenario
from astrosim.visualization.dashboard import plot_dashboard
from astrosim.visualization.web import render_web_dashboard


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AstroSim habitat simulator")
    parser.add_argument(
        "scenario",
        type=Path,
        nargs="?",
        help="Path to scenario YAML or JSON file",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("output"),
        help="Directory for results",
    )
    parser.add_argument("--no-plot", action="store_true", help="Skip matplotlib dashboard")
    parser.add_argument("--web", action="store_true", help="Generate HTML web dashboard")
    parser.add_argument(
        "--monte-carlo",
        type=int,
        metavar="N",
        help="Run N Monte Carlo perturbation runs and write summary JSON",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for Monte Carlo runs",
    )
    parser.add_argument(
        "--ask",
        type=str,
        metavar="PROMPT",
        help="NL scenario edit (dry-run JSON unless --write)",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="With --ask, write patched YAML instead of dry-run JSON",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="With --ask --write, overwrite existing output file",
    )
    parser.add_argument(
        "--output",
        type=Path,
        metavar="PATH",
        help="Output path for --ask --write (default: <stem>.patched.yaml)",
    )
    parser.add_argument(
        "--trade-study",
        action="store_true",
        help="Run solar vs battery Pareto trade study and write CSV",
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Write study_report.md (+ JSON sidecar) to output dir",
    )
    parser.add_argument(
        "--compare",
        nargs="+",
        type=Path,
        metavar="SCENARIO",
        help="Compare multiple scenarios and print metric table",
    )
    parser.add_argument(
        "--metrics",
        nargs="+",
        default=["energy.net_kwh", "mass.net_import_kg", "reliability.success"],
        help="Metrics for --compare",
    )
    return parser


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    return build_parser().parse_args(argv)


def output_stem(config_name: str) -> str:
    return config_name.replace(" ", "_").lower()


def run_from_args(args: argparse.Namespace) -> Path:
    """Execute simulation and writes outputs; returns output directory."""
    config = load_scenario(args.scenario)
    simulator = load_and_build(args.scenario)
    result = simulator.run()

    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)
    name = output_stem(result.config.name)

    export_json(result, out / f"{name}.json")
    export_csv(result, out / f"{name}.csv")
    if not args.no_plot:
        plot_dashboard(result, out / f"{name}_dashboard.png")
    if args.web:
        render_web_dashboard(result, out / f"{name}_dashboard.html")

    if args.report:
        from astrosim.export.study_report import render_study_report

        report_path = render_study_report(
            result,
            output_path=out / "study_report.md",
            scenario_path=str(args.scenario),
        )
        print(f"Study report: {report_path.resolve()}")

    hooks = AIHooks()
    insights = hooks.generate_insights(InsightRequest(result=result))
    print(insights)

    suggestions = hooks.suggest_optimizations(result)
    if suggestions:
        print("\nOptimization suggestions:")
        for suggestion in suggestions:
            print(
                f"  {suggestion.parameter}: "
                f"{suggestion.current_value} -> {suggestion.suggested_value} "
                f"({suggestion.rationale})"
            )

    if args.monte_carlo:
        mc_result = MonteCarloRunner(
            base_config=config,
            build_simulator=build_simulator,
            seed=args.seed,
        ).run(num_runs=args.monte_carlo)
        mc_path = out / f"{name}_monte_carlo_summary.json"
        mc_path.write_text(json.dumps(mc_result.summary, indent=2))
        print(f"\nMonte Carlo: {mc_result.num_runs} runs written to {mc_path.name}")

    print(f"\nResults written to {out.resolve()}")
    return out


def handle_trade_study(scenario_path: Path, output_dir: Path) -> None:
    from astrosim.analysis.pareto import export_trade_study_csv, run_trade_study

    config = load_scenario(scenario_path)
    config.duration_hours = min(config.duration_hours, 168)
    result = run_trade_study(
        config,
        build_simulator,
        param_x="solar_array_kw",
        param_y="battery_kwh",
        values_x=[60.0, 80.0, 100.0, 120.0],
        values_y=[200.0, 400.0, 600.0],
        metric_a="energy.net_kwh",
        metric_b="reliability.success",
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    path = export_trade_study_csv(result, output_dir / "trade_study.csv")
    print(f"Trade study: {len(result.points)} points, {len(result.pareto_points)} Pareto-optimal")
    print(f"Written to {path.resolve()}")


def handle_ask(
    scenario_path: Path,
    prompt: str,
    *,
    write: bool = False,
    force: bool = False,
    output: Path | None = None,
) -> None:
    import yaml

    from astrosim.ai.scenario_editor import apply_patch, parse_edit_intent

    data = yaml.safe_load(scenario_path.read_text())
    patch = parse_edit_intent(prompt)
    updated = apply_patch(data, patch)

    if write:
        out_path = output or scenario_path.with_name(f"{scenario_path.stem}.patched.yaml")
        if out_path.exists() and not force:
            print(f"Refusing to overwrite {out_path}; use --force", file=sys.stderr)
            raise SystemExit(1)
        out_path.write_text(yaml.safe_dump(updated, sort_keys=False))
        print(f"Wrote {out_path.resolve()}")
        return

    print(json.dumps({"dry_run": True, "patch": patch.__dict__, "scenario": updated}, indent=2))


def handle_compare(paths: list[Path], metrics: list[str], output_dir: Path) -> None:
    from astrosim.analysis.compare import (
        compare_scenarios,
        export_compare_csv,
        format_compare_table,
    )

    result = compare_scenarios(paths, metrics)
    print(format_compare_table(result))
    for err in result.errors:
        print(f"WARN: {err}", file=sys.stderr)
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = export_compare_csv(result, output_dir / "scenario_compare.csv")
    print(f"Compare CSV: {csv_path.resolve()}")


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    if args.compare:
        handle_compare(args.compare, args.metrics, args.output_dir)
        return
    if args.ask:
        if args.scenario is None:
            print("scenario file required with --ask", file=sys.stderr)
            raise SystemExit(2)
        handle_ask(
            args.scenario,
            args.ask,
            write=args.write,
            force=args.force,
            output=args.output,
        )
        return
    if args.trade_study:
        if args.scenario is None:
            print("scenario file required with --trade-study", file=sys.stderr)
            raise SystemExit(2)
        handle_trade_study(args.scenario, args.output_dir)
        return
    if args.scenario is None:
        print("scenario file required", file=sys.stderr)
        raise SystemExit(2)
    run_from_args(args)


if __name__ == "__main__":
    main()