from __future__ import annotations

from app.models import Recipe, RecipeAnalysis


def render_discovery(recipes: list[Recipe]) -> str:
    lines = [
        "# Demo Recipe Discovery",
        "",
        "| recipe | mode | domain | framework | profiling | focus |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for recipe in recipes:
        lines.append(
            f"| {recipe.recipe_name} | {recipe.mode} | {recipe.domain} | {recipe.framework} | "
            f"{'yes' if recipe.profiling_supported else 'no'} | {', '.join(recipe.expected_focus)} |"
        )
    return "\n".join(lines)


def render_report(analyses: list[RecipeAnalysis]) -> str:
    lines = [
        "# Auto Analysis Demo Report",
        "",
        "这个输出模拟了新 project 的第一版报告层：统一看 recipe、run、profiling、结论和验证。",
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
                f"- 入口: `{recipe.entry_command}`",
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
        "# Project Migration Plan",
        "",
        "当前项目已经完成了目标定义、试点选择和 V1 规范，新 project 不需要重写分析，而是要把分析结果落成代码结构。",
        "",
        "## 从当前 project 映射到新 project",
        "",
        "| 当前内容 | 新项目对应模块 | 说明 |",
        "| --- | --- | --- |",
        "| 01_goals_and_closures.md | `analysis/` + `reports/` | 把闭环目标变成真正的分析输出接口 |",
        "| 03_recipe_inventory.md | `recipes/` | 把试点样例变成可登记、可发现的标准资产 |",
        "| 04_v1_integration_spec.md | `adapters/` + `schema/` | 把字段定义、运行描述和 profiling 挂接代码化 |",
        "| 05_recipe_admission_rules.md | `validators/` | 把合入规则变成自动校验，而不是人工检查 |",
        "",
        "## 推荐的三阶段改造",
        "",
        "1. Phase 1: 先把 `recipe -> run -> profiling -> report` 打通，哪怕底层运行还是 mock 数据。",
        "2. Phase 2: 增加真实 adapter，把外部 recipe 仓映射成统一入口，并把 run 产物落到统一目录。",
        "3. Phase 3: 在统一数据上做规则分析、收益验证和跨模型归因，逐步长成 CANN/芯片输入层。",
        "",
        "## 新项目最小目录",
        "",
        "```text",
        "new_project/",
        "  recipes/",
        "    hunyuan_video/",
        "      recipe.yaml",
        "  adapters/",
        "    base.py",
        "    infer_adapter.py",
        "    train_adapter.py",
        "  runs/",
        "    <run_id>/",
        "      run.json",
        "      metrics.json",
        "      logs/",
        "  profiling/",
        "    <run_id>.json",
        "  analysis/",
        "    rules.py",
        "    validator.py",
        "  reports/",
        "    markdown.py",
        "```",
        "",
        "## demo 的意义",
        "",
        "这个 demo 证明了：下一步不是继续写分析文档，而是开始沉淀 schema、adapter 和 report 三层。",
    ]
    return "\n".join(lines)
