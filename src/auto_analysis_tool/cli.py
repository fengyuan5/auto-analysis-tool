from __future__ import annotations

import argparse
from pathlib import Path

from auto_analysis_tool.analyzer import Analyzer
from auto_analysis_tool.reporting import (
    render_discovery,
    render_migration_plan,
    render_report,
    render_validation,
)
from auto_analysis_tool.repository import Repository


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Auto analysis tool prototype")
    parser.add_argument(
        "--data-dir",
        default=str(Path(__file__).resolve().parents[2] / "examples"),
        help="Directory containing recipes, runs and profiling data.",
    )
    parser.add_argument(
        "command",
        choices=["discover", "report", "migration", "validate"],
        help="Command to execute.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    data_dir = Path(args.data_dir).resolve()
    repository = Repository(data_dir)

    if args.command == "discover":
        recipes = repository.load_recipes()
        print(render_discovery(recipes, data_dir))
        return

    if args.command == "report":
        analyzer = Analyzer()
        recipes = repository.load_recipes()
        analyses = [analyzer.analyze_recipe(recipe, repository) for recipe in recipes]
        print(render_report(analyses))
        return

    if args.command == "migration":
        print(render_migration_plan())
        return

    if args.command == "validate":
        print(render_validation(repository.validate_recipes()))
        return
