from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Recipe:
    recipe_name: str
    model_name: str
    task_type: str
    mode: str
    domain: str
    hardware_target: str
    cann_version: str
    framework: str
    entry_command: str
    profiling_supported: bool
    baseline_run_id: str
    optimized_run_id: str
    summary: str
    expected_focus: list[str]


@dataclass(frozen=True)
class RunRecord:
    run_id: str
    recipe_name: str
    variant: str
    status: str
    run_mode: str
    device_count: int
    latency_ms: float | None
    throughput: float | None
    memory_peak_gb: float | None
    accuracy_metric: str | None
    accuracy_value: float | None
    notes: str


@dataclass(frozen=True)
class ProfilingRecord:
    run_id: str
    host_wait_ratio: float
    kernel_utilization: float
    io_wait_ratio: float
    launch_overhead_ms: float
    dominant_issue: str


@dataclass(frozen=True)
class Finding:
    title: str
    evidence: str
    recommendation: str
    expected_gain: str


@dataclass(frozen=True)
class ValidationDiff:
    summary: str
    metric_diffs: dict[str, str]
    is_effective: bool


@dataclass(frozen=True)
class RecipeAnalysis:
    recipe: Recipe
    baseline: RunRecord
    optimized: RunRecord
    baseline_profiling: ProfilingRecord
    optimized_profiling: ProfilingRecord
    findings: list[Finding]
    validation: ValidationDiff


def recipe_from_dict(data: dict[str, Any]) -> Recipe:
    return Recipe(
        recipe_name=data["recipe_name"],
        model_name=data["model_name"],
        task_type=data["task_type"],
        mode=data["mode"],
        domain=data["domain"],
        hardware_target=data["hardware_target"],
        cann_version=data["cann_version"],
        framework=data["framework"],
        entry_command=data["entry_command"],
        profiling_supported=data["profiling_supported"],
        baseline_run_id=data["baseline_run_id"],
        optimized_run_id=data["optimized_run_id"],
        summary=data["summary"],
        expected_focus=data["expected_focus"],
    )


def run_from_dict(data: dict[str, Any]) -> RunRecord:
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


def profiling_from_dict(data: dict[str, Any]) -> ProfilingRecord:
    return ProfilingRecord(
        run_id=data["run_id"],
        host_wait_ratio=data["host_wait_ratio"],
        kernel_utilization=data["kernel_utilization"],
        io_wait_ratio=data["io_wait_ratio"],
        launch_overhead_ms=data["launch_overhead_ms"],
        dominant_issue=data["dominant_issue"],
    )
