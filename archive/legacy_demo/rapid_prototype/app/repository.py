from __future__ import annotations

import json
from pathlib import Path

from app.models import ProfilingRecord, Recipe, RunRecord, profiling_from_dict, recipe_from_dict, run_from_dict


class DemoRepository:
    def __init__(self, data_dir: Path) -> None:
        self.data_dir = data_dir

    def load_recipes(self) -> list[Recipe]:
        recipe_files = sorted((self.data_dir / "recipes").glob("*/recipe.json"))
        return [recipe_from_dict(self._read_json(path)) for path in recipe_files]

    def load_run(self, run_id: str) -> RunRecord:
        return run_from_dict(self._read_json(self.data_dir / "runs" / f"{run_id}.json"))

    def load_profiling(self, run_id: str) -> ProfilingRecord:
        return profiling_from_dict(
            self._read_json(self.data_dir / "profiling" / f"{run_id}.json")
        )

    @staticmethod
    def _read_json(path: Path) -> dict:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
