from __future__ import annotations

import json
from pathlib import Path

from auto_analysis_tool.models import (
    EntryPoint,
    MetricSpec,
    OutputSpec,
    ProfilingRecord,
    ProfilingSpec,
    Recipe,
    RunRecord,
)
from auto_analysis_tool.validators import validate_recipe_data


class Repository:
    def __init__(self, data_dir: Path) -> None:
        self.data_dir = data_dir

    def load_recipes(self) -> list[Recipe]:
        recipe_files = sorted((self.data_dir / "recipes").glob("*/recipe.yaml"))
        recipes: list[Recipe] = []
        for path in recipe_files:
            raw = self._read_structured_file(path)
            errors = validate_recipe_data(raw)
            if errors:
                joined = ", ".join(errors)
                raise ValueError(f"invalid recipe file {path}: {joined}")
            recipes.append(self._recipe_from_dict(raw))
        return recipes

    def validate_recipes(self) -> list[tuple[str, list[str]]]:
        results: list[tuple[str, list[str]]] = []
        for path in sorted((self.data_dir / "recipes").glob("*/recipe.yaml")):
            raw = self._read_structured_file(path)
            errors = validate_recipe_data(raw)
            errors.extend(self._validate_recipe_links(raw))
            results.append((path.parent.name, errors))
        return results

    def load_run(self, run_id: str) -> RunRecord:
        data = self._read_json_file(self.data_dir / "runs" / f"{run_id}.json")
        return RunRecord(
            run_id=data["run_id"],
            recipe_name=data["recipe_name"],
            variant=data["variant"],
            status=data["status"],
            run_mode=data["run_mode"],
            device_count=data["device_count"],
            latency_ms=data.get("latency_ms"),
            throughput=data.get("throughput"),
            memory_peak_gb=data.get("memory_peak_gb"),
            accuracy_metric=data.get("accuracy_metric"),
            accuracy_value=data.get("accuracy_value"),
            notes=data["notes"],
        )

    def load_profiling(self, run_id: str) -> ProfilingRecord:
        data = self._read_json_file(self.data_dir / "profiling" / f"{run_id}.json")
        return ProfilingRecord(
            run_id=data["run_id"],
            host_wait_ratio=data["host_wait_ratio"],
            kernel_utilization=data["kernel_utilization"],
            io_wait_ratio=data["io_wait_ratio"],
            launch_overhead_ms=data["launch_overhead_ms"],
            dominant_issue=data["dominant_issue"],
        )

    def _recipe_from_dict(self, data: dict) -> Recipe:
        entrypoint = EntryPoint(**data["entrypoint"])
        outputs = OutputSpec(**data["outputs"])
        profiling = ProfilingSpec(**data["profiling"])
        metrics = MetricSpec(**data["metrics"])
        return Recipe(
            recipe_name=data["recipe_name"],
            model_name=data["model_name"],
            task_type=data["task_type"],
            mode=data["mode"],
            domain=data["domain"],
            hardware_target=data["hardware_target"],
            cann_version=data["cann_version"],
            framework=data["framework"],
            python_version=data["python_version"],
            entrypoint=entrypoint,
            upstream_repos=data.get("upstream_repos", []),
            model_weights=data.get("model_weights", []),
            datasets=data.get("datasets", []),
            container=data.get("container", ""),
            requires_git_lfs=data.get("requires_git_lfs", False),
            outputs=outputs,
            profiling=profiling,
            metrics=metrics,
            comparison_baseline=data["comparison_baseline"],
            baseline_run_id=data["baseline_run_id"],
            optimized_run_id=data["optimized_run_id"],
            summary=data.get("summary", ""),
            expected_focus=data.get("expected_focus", []),
        )

    def _validate_recipe_links(self, data: dict) -> list[str]:
        errors: list[str] = []
        recipe_name = data.get("recipe_name", "<unknown>")
        run_ids = [data.get("baseline_run_id"), data.get("optimized_run_id")]

        for run_id in run_ids:
            if not run_id:
                continue

            run_path = self.data_dir / "runs" / f"{run_id}.json"
            profiling_path = self.data_dir / "profiling" / f"{run_id}.json"

            if not run_path.exists():
                errors.append(f"{recipe_name}: missing run file for {run_id}")
            if not profiling_path.exists():
                errors.append(f"{recipe_name}: missing profiling file for {run_id}")

        return errors

    @staticmethod
    def _read_structured_file(path: Path) -> dict:
        # Prototype version: recipe.yaml uses JSON-compatible YAML so we can stay dependency-free.
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    @staticmethod
    def _read_json_file(path: Path) -> dict:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
