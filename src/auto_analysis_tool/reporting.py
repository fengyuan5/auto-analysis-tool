from __future__ import annotations

from pathlib import Path

from auto_analysis_tool.models import Recipe, RecipeAnalysis


def render_discovery(recipes: list[Recipe], data_dir: Path) -> str:
    lines = [
        "# Recipe Discovery",
        "",
        f"data_dir: `{data_dir}`",
        "",
        "| recipe | mode | domain | framework | profiling | focus |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for recipe in recipes:
        lines.append(
            f"| {recipe.recipe_name} | {recipe.mode} | {recipe.domain} | {recipe.framework} | "
            f"{'yes' if recipe.profiling.supported else 'no'} | {', '.join(recipe.expected_focus)} |"
        )
    return "\n".join(lines)


def render_report(analyses: list[RecipeAnalysis]) -> str:
    lines = [
        "# Auto Analysis Report",
        "",
        "这个输出对应新 project 的报告层：统一查看 recipe、run、profiling、结论和验证。",
        "",
    ]

    for analysis in analyses:
        recipe = analysis.recipe
        lines.extend(
            [
                f"## {recipe.recipe_name}",
                "",
                f"- 模型: `{recipe.model_name}`",
                f"- 场景: `{recipe.task_type}` / `{recipe.mode}` / `{recipe.domain}`",
                f"- 硬件: `{recipe.hardware_target}` / CANN `{recipe.cann_version}`",
                f"- 入口: `{recipe.entrypoint.type} {recipe.entrypoint.path}`",
                f"- 摘要: {recipe.summary}",
                "",
                "### Findings",
                "",
            ]
        )
        for finding in analysis.findings:
            lines.append(
                f"- {finding.title}: {finding.evidence}；建议 {finding.recommendation} 预期收益是 {finding.expected_gain}"
            )
        lines.extend(["", "### Validation", ""])
        for metric_name, diff in analysis.validation.metric_diffs.items():
            lines.append(f"- {metric_name}: {diff}")
        lines.append(f"- closed_loop: {'effective' if analysis.validation.is_effective else 'needs more data'}")
        lines.append(f"- note: {analysis.validation.summary}")
        lines.append("")

    return "\n".join(lines)


def render_migration_plan() -> str:
    lines = [
        "# Migration Plan",
        "",
        "这个仓库的目标不是再写一版大文档，而是把当前分析文档落成可扩展 project。",
        "",
        "## 从当前内容映射到完整项目",
        "",
        "| 当前内容 | 新项目模块 | 作用 |",
        "| --- | --- | --- |",
        "| `01_goals_and_closures.md` | `analysis/` + `reporting.py` | 闭环目标落成输出接口 |",
        "| `03_recipe_inventory.md` | `examples/recipes/` | 试点样例落成标准资产 |",
        "| `04_v1_integration_spec.md` | `models.py` + `repository.py` | schema 与运行描述代码化 |",
        "| `05_recipe_admission_rules.md` | `validators.py` | 合入规则自动校验 |",
        "",
        "## 推荐演进顺序",
        "",
        "1. Phase 1: 先把 schema、report、validate 三层稳定下来。",
        "2. Phase 2: 接真实外部 recipe 仓，新增 adapter 层和运行产物落盘。",
        "3. Phase 3: 增加跨模型聚合分析，把单模型信号提升为 CANN/芯片输入。",
        "",
        "## 适合推 GitHub 的原因",
        "",
        "1. 已有 README、包结构、示例数据、测试和 CI。",
        "2. 代码和战略文档分层清楚，不会混成一次性讨论材料。",
        "3. 下一步接真实 recipe 时，不需要重写项目骨架。",
    ]
    return "\n".join(lines)


def render_validation(results: list[tuple[str, list[str]]]) -> str:
    lines = [
        "# Recipe Validation",
        "",
    ]
    for recipe_name, errors in results:
        if errors:
            lines.append(f"- {recipe_name}: invalid")
            for error in errors:
                lines.append(f"  - {error}")
        else:
            lines.append(f"- {recipe_name}: valid")
    return "\n".join(lines)
