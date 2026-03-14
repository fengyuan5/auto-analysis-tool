from app.analyzer import DemoAnalyzer
from app.reporter import render_discovery, render_migration_plan, render_report
from app.repository import DemoRepository

import argparse
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Auto analysis demo")
    parser.add_argument(
        "command",
        choices=["discover", "report", "migration"],
        help="Demo command to execute",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parent
    repository = DemoRepository(base_dir / "data")
    analyzer = DemoAnalyzer()

    recipes = repository.load_recipes()

    if args.command == "discover":
        print(render_discovery(recipes))
        return

    if args.command == "report":
        analyses = [analyzer.analyze_recipe(recipe, repository) for recipe in recipes]
        print(render_report(analyses))
        return

    if args.command == "migration":
        print(render_migration_plan())
        return


if __name__ == "__main__":
    main()
