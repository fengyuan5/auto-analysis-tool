from __future__ import annotations

from auto_analysis_tool.models import Finding, Recipe, RecipeAnalysis, ValidationDiff
from auto_analysis_tool.repository import Repository


class Analyzer:
    def analyze_recipe(self, recipe: Recipe, repository: Repository) -> RecipeAnalysis:
        baseline = repository.load_run(recipe.baseline_run_id)
        optimized = repository.load_run(recipe.optimized_run_id)
        baseline_profiling = repository.load_profiling(recipe.baseline_run_id)
        optimized_profiling = repository.load_profiling(recipe.optimized_run_id)

        findings = self._build_findings(recipe, baseline_profiling)
        validation = self._build_validation(recipe, baseline, optimized)

        return RecipeAnalysis(
            recipe=recipe,
            baseline=baseline,
            optimized=optimized,
            baseline_profiling=baseline_profiling,
            optimized_profiling=optimized_profiling,
            findings=findings,
            validation=validation,
        )

    def _build_findings(self, recipe: Recipe, profiling) -> list[Finding]:
        findings: list[Finding] = []

        if profiling.host_wait_ratio >= 0.20:
            findings.append(
                Finding(
                    title="Host wait 偏高",
                    evidence=f"host_wait_ratio={profiling.host_wait_ratio:.0%}",
                    recommendation="把前处理、权重准备和同步点前移或异步化。",
                    expected_gain="降低端到端抖动，提升吞吐稳定性。",
                )
            )

        if profiling.kernel_utilization <= 0.65:
            findings.append(
                Finding(
                    title="Kernel utilization 偏低",
                    evidence=f"kernel_utilization={profiling.kernel_utilization:.0%}",
                    recommendation="优先检查图模式、算子融合和 batch 规格，避免执行图过碎。",
                    expected_gain="提升有效利用率，减少 launch overhead。",
                )
            )

        if profiling.io_wait_ratio >= 0.15:
            findings.append(
                Finding(
                    title="I/O 等待明显",
                    evidence=f"io_wait_ratio={profiling.io_wait_ratio:.0%}",
                    recommendation="统一本地缓存、预取和模型权重准备路径。",
                    expected_gain="缩短 warmup 时间并提升稳定段表现。",
                )
            )

        if recipe.mode == "train":
            findings.append(
                Finding(
                    title="训练收益字段仍需扩充",
                    evidence="当前已覆盖 throughput、checkpoint 和 reward，但 loss 曲线与超参变更还未标准化。",
                    recommendation="把训练超参、关键 checkpoint 和收益曲线写入统一 run schema。",
                    expected_gain="支撑训练样例横向比较和后续优化 agent。",
                )
            )

        if not findings:
            findings.append(
                Finding(
                    title="运行链路基本正常",
                    evidence=f"dominant_issue={profiling.dominant_issue}",
                    recommendation="继续补更多 profiling 指标并扩大规则覆盖面。",
                    expected_gain="提升自动分析解释能力。",
                )
            )

        return findings

    def _build_validation(self, recipe: Recipe, baseline, optimized) -> ValidationDiff:
        metric_diffs: dict[str, str] = {}

        if baseline.latency_ms is not None and optimized.latency_ms is not None:
            latency_gain = (baseline.latency_ms - optimized.latency_ms) / baseline.latency_ms
            metric_diffs["latency"] = (
                f"{baseline.latency_ms:.1f} ms -> {optimized.latency_ms:.1f} ms "
                f"({latency_gain:+.1%})"
            )

        if baseline.throughput is not None and optimized.throughput is not None:
            throughput_gain = (optimized.throughput - baseline.throughput) / baseline.throughput
            metric_diffs["throughput"] = (
                f"{baseline.throughput:.1f} -> {optimized.throughput:.1f} "
                f"({throughput_gain:+.1%})"
            )

        if baseline.memory_peak_gb is not None and optimized.memory_peak_gb is not None:
            memory_change = (optimized.memory_peak_gb - baseline.memory_peak_gb) / baseline.memory_peak_gb
            metric_diffs["memory_peak"] = (
                f"{baseline.memory_peak_gb:.1f} GB -> {optimized.memory_peak_gb:.1f} GB "
                f"({memory_change:+.1%})"
            )

        if (
            baseline.accuracy_metric
            and baseline.accuracy_value is not None
            and optimized.accuracy_value is not None
        ):
            metric_diffs[baseline.accuracy_metric] = (
                f"{baseline.accuracy_value:.3f} -> {optimized.accuracy_value:.3f}"
            )

        is_effective = False
        throughput_diff = metric_diffs.get("throughput", "")
        latency_diff = metric_diffs.get("latency", "")
        if "+" in throughput_diff or ("latency" in metric_diffs and "+" in latency_diff):
            is_effective = True

        summary = (
            f"{recipe.recipe_name} 已形成 baseline -> optimized 的最小验证闭环，"
            "后续只需要把 mock run 换成真实 adapter。"
        )

        return ValidationDiff(summary=summary, metric_diffs=metric_diffs, is_effective=is_effective)
