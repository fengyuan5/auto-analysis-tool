from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EntryPoint:
    type: str
    path: str
    workdir: str
    default_args: list[str]


@dataclass(frozen=True)
class OutputSpec:
    log_dir: str
    result_dir: str
    checkpoint_dir: str


@dataclass(frozen=True)
class ProfilingSpec:
    supported: bool
    enable_mode: str
    enable_flag: str
    notes: str


@dataclass(frozen=True)
class MetricSpec:
    performance: list[str]
    accuracy: list[str]


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
    python_version: str
    entrypoint: EntryPoint
    upstream_repos: list[str]
    model_weights: list[str]
    datasets: list[str]
    container: str
    requires_git_lfs: bool
    outputs: OutputSpec
    profiling: ProfilingSpec
    metrics: MetricSpec
    comparison_baseline: str
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
