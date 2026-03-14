from __future__ import annotations

import unittest
from pathlib import Path
import sys
import tempfile
import json

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from auto_analysis_tool.repository import Repository
from auto_analysis_tool.validators import validate_recipe_data


class RepositoryTest(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = Repository(ROOT / "examples")

    def test_load_recipes(self) -> None:
        recipes = self.repository.load_recipes()
        self.assertEqual(3, len(recipes))
        self.assertEqual("hunyuan_video", recipes[0].recipe_name)

    def test_validate_recipes(self) -> None:
        results = dict(self.repository.validate_recipes())
        self.assertEqual([], results["hunyuan_video"])
        self.assertEqual([], results["pi0_infer_with_torch"])
        self.assertEqual([], results["qwen2_5_rl_demo"])

    def test_validate_recipe_data_rejects_invalid_mode(self) -> None:
        errors = validate_recipe_data({"mode": "bad_mode"})
        self.assertIn("invalid mode: bad_mode", errors)

    def test_validate_recipes_reports_missing_linked_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_root = Path(tmp_dir)
            (tmp_root / "recipes" / "broken").mkdir(parents=True)
            (tmp_root / "runs").mkdir()
            (tmp_root / "profiling").mkdir()

            recipe_data = {
                "recipe_name": "broken",
                "model_name": "BrokenModel",
                "task_type": "demo",
                "mode": "infer",
                "domain": "other",
                "hardware_target": "Ascend 910B",
                "cann_version": "8.x",
                "framework": "PyTorch",
                "python_version": "3.10",
                "entrypoint": {
                    "type": "shell",
                    "path": "run.sh",
                    "workdir": ".",
                    "default_args": [],
                },
                "outputs": {
                    "log_dir": "outputs/logs",
                    "result_dir": "outputs/results",
                    "checkpoint_dir": "outputs/checkpoints",
                },
                "profiling": {
                    "supported": False,
                    "enable_mode": "none",
                    "enable_flag": "",
                    "notes": "",
                },
                "metrics": {
                    "performance": ["latency_ms"],
                    "accuracy": [],
                },
                "comparison_baseline": "default",
                "baseline_run_id": "broken_baseline",
                "optimized_run_id": "broken_optimized",
            }

            recipe_path = tmp_root / "recipes" / "broken" / "recipe.yaml"
            recipe_path.write_text(json.dumps(recipe_data), encoding="utf-8")

            repository = Repository(tmp_root)
            results = dict(repository.validate_recipes())

            self.assertIn("broken: missing run file for broken_baseline", results["broken"])
            self.assertIn("broken: missing profiling file for broken_optimized", results["broken"])
