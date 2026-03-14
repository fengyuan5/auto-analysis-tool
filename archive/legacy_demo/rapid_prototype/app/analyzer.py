from __future__ import annotations

from app.models import Finding, Recipe, RecipeAnalysis, ValidationDiff
from app.repository import DemoRepository


class DemoAnalyzer:
    def analyze_recipe(self, recipe: Recipe, repository: DemoRepository) -> RecipeAnalysis:
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
                    title="Host 侧等待偏高",
                    evidence=f"host_wait_ratio={profiling.host_wait_ratio:.0%}",
                    recommendation="把数据预处理、权重加载和 host-device 同步点前移或异步化。",
                    expected_gain="降低端到端时延抖动，提升吞吐稳定性。",
                )
            )

        if profiling.kernel_utilization <= 0.65:
            findings.append(
                Finding(
                    title="算子利用率偏低",
                    evidence=f"kernel_utilization={profiling.kernel_utilization:.0%}",
                    recommendation="优先检查图模式、算子融合和 batch 规格，避免过碎的执行图。",
                    expected_gain="提升芯片有效利用率，减少 launch 开销。",
                )
            )

        if profiling.io_wait_ratio >= 0.15:
            findings.append(
                Finding(
                    title="I/O 等待明显",
                    evidence=f"io_wait_ratio={profiling.io_wait_ratio:.0%}",
                    recommendation="把模型权重、数据和中间产物路径纳入统一缓存和本地预取策略。",
                    expected_gain="缩短 warmup 和稳定阶段切换时间。",
                )
            )

        if recipe.mode == "train":
            findings.append(
                Finding(
                    title="训练样例需补统一训练收益抽象",
                    evidence="当前 demo 里已经有日志、checkpoint 和吞吐，但还缺 loss/奖励曲线的统一字段。",
                    recommendation="把训练配置、关键超参、checkpoint 路径和收益指标纳入统一 run schema。",
                    expected_gain="为后续训练优化 agent 和横向对比打底。",
                )
            )

        if not findings:
            findings.append(
                Finding(
                    title="基础运行正常",
                    evidence=f"dominant_issue={profiling.dominant_issue}",
                    recommendation="继续增加更细粒度 profiling 指标，扩大规则覆盖面。",
                    expected_gain="提高自动分析解释力。",
                )
            )

        return findings

    def _build_validation(self, recipe: Recipe, baseline, optimized) -> ValidationDiff:
        metric_diffs: dict[str, str] = {}

        if baseline.latency_ms and optimized.latency_ms:
            latency_gain = (baseline.latency_ms - optimized.latency_ms) / baseline.latency_ms
            metric_diffs["latency"] = f"{baseline.latency_ms:.1f} ms -> {optimized.latency_ms:.1f} ms ({latency_gain:+.1%})"

        if baseline.throughput and optimized.throughput:
            throughput_gain = (optimized.throughput - baseline.throughput) / baseline.throughput
            metric_diffs["throughput"] = f"{baseline.throughput:.1f} -> {optimized.throughput:.1f} ({throughput_gain:+.1%})"

        if baseline.memory_peak_gb and optimized.memory_peak_gb:
            memory_change = (optimized.memory_peak_gb - baseline.memory_peak_gb) / baseline.memory_peak_gb
            metric_diffs["memory_peak"] = f"{baseline.memory_peak_gb:.1f} GB -> {optimized.memory_peak_gb:.1f} GB ({memory_change:+.1%})"

        if baseline.accuracy_value is not None and optimized.accuracy_value is not None and baseline.accuracy_metric:
            metric_diffs[baseline.accuracy_metric] = (
                f"{baseline.accuracy_value:.3f} -> {optimized.accuracy_value:.3f}"
            )

        is_effective = any("+" in diff for key, diff in metric_diffs.items() if key == "throughput") or any(
            "-" in diff for key, diff in metric_diffs.items() if key == "latency"
        )

        summary = (
            f"{recipe.recipe_name} 已形成 baseline -> optimized 的最小验证闭环，可继续扩成真实执行流水线。"
        )

        return ValidationDiff(summary=summary, metric_diffs=metric_diffs, is_effective=is_effective)
