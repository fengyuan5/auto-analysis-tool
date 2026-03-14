# Auto Analysis Tool

面向昇腾/CANN 生态的 recipe 标准化、数据库建设和分析原型项目。

## 目的

这个仓库的目标，不是单纯收集一些 recipe，也不是只做一次性的 profiling 分析。

它要解决的是：

1. 把不同来源的 recipe 样例统一抽取、统一运行、统一入库。
2. 建立可持续演进的统一数据库。
3. 基于这套数据库，支撑上层 agent 的建设和迭代。

当前已经明确的上层能力包括：

1. 统一数据库构建
2. 模型优化 agent
3. bound 搜索 agent
4. 芯片建议 agent
5. profiling 分析 agent
6. 其他基于数据库的自动分析能力

一句话说，这个仓库要把“分散、能跑但难复用的 recipe 样例”，逐步变成“可被平台理解、可被数据库吸收、可被 agent 消费的标准资产”。

## Recipe 为什么要标准化

如果没有统一数据库，后续很多工作都会停留在人工经验层：

1. recipe 信息散在 README、脚本和外部仓里，难以稳定抽取。
2. 运行入口不统一，样例之间无法形成批量接入和横向比较。
3. profiling、结果和优化记录难以结构化沉淀。
4. 单模型经验很难沉淀成可复用知识，更难支撑上层 agent。

因此这个项目首先要求 recipe 具备最小闭环：

`recipe -> run -> profiling -> analysis -> validation -> database -> agents`

要进入这个闭环，recipe 至少要逐步具备：

1. `recipe.yaml`
2. `README.md`
3. 统一入口 `run.sh` 或 `run.py`
4. 依赖声明 `requirements.txt` / `environment.yml` / `Dockerfile`
5. baseline 和 optimized 的 `run.json`
6. 对应运行的 `profiling.json`

## 当前项目提供了什么

围绕上面的目标，这个仓库当前提供了 4 类东西：

1. 设计原则和规则文档
   说明为什么要做数据库、为什么要有合入规则、V1 的最小闭环是什么。
2. 迁移操作手册和模板
   让后续同学知道新增一个模型时，具体该补什么文件、怎么跑校验。
3. 示例资产
   用 3 个代表样例演示推理、训练和具身智能场景怎么落到统一结构。
4. 最小代码骨架
   提供 `discover`、`validate`、`report` 这条最小链路，证明 schema 和闭环是可执行的。

当前首批示例样例：

1. `hunyuan_video`
2. `qwen2_5_rl_demo`
3. `pi0_infer_with_torch`

## 我是不同角色，先看什么

### 1. 想理解设计原则的同学

1. [项目目标与闭环](docs/strategy/01_goals_and_closures.md)
2. [执行推进方案](docs/strategy/02_execution_plan.md)
3. [项目架构说明](docs/architecture.md)

### 2. 准备后续合入 recipe 的同学

1. [新增模型操作手册](docs/how_to_add_a_model.md)
2. [recipe 合入规则](docs/strategy/05_recipe_admission_rules.md)
3. [模板说明](examples/templates/README.md)
4. [试点 recipe 盘点](docs/strategy/03_recipe_inventory.md)

### 3. 准备一起共建数据库和后续 agent 的同学

1. [V1 接入规范](docs/strategy/04_v1_integration_spec.md)
2. [recipe 合入规则](docs/strategy/05_recipe_admission_rules.md)
3. [数据契约](docs/data_contract.md)
4. [数据模型](src/auto_analysis_tool/models.py)
5. [数据加载层](src/auto_analysis_tool/repository.py)
6. [规则校验层](src/auto_analysis_tool/validators.py)

## 快速开始

```bash
PYTHONPATH=src python3 -m auto_analysis_tool discover
PYTHONPATH=src python3 -m auto_analysis_tool validate
PYTHONPATH=src python3 -m auto_analysis_tool report
python3 -m unittest discover -s tests
```

## 新增一个模型时直接看

1. [新增模型操作手册](docs/how_to_add_a_model.md)
2. [recipe 合入规则](docs/strategy/05_recipe_admission_rules.md)
3. [recipe 模板](examples/templates/recipe.yaml)
4. [README 模板](examples/templates/RECIPE_README.md)
5. [run.sh 模板](examples/templates/run.sh)
6. [requirements.txt 模板](examples/templates/requirements.txt)
7. [run 模板](examples/templates/run.json)
8. [profiling 模板](examples/templates/profiling.json)

## 文档入口

1. [文档导航](docs/README.md)
2. [策略文档入口](docs/strategy/README.md)
3. [新增模型操作手册](docs/how_to_add_a_model.md)
4. [数据契约](docs/data_contract.md)
5. [项目架构说明](docs/architecture.md)
6. [迁移说明](docs/migration.md)

## 仓库结构

```text
.
├── README.md
├── src/auto_analysis_tool/
├── examples/
├── docs/
├── tests/
├── .github/workflows/
└── archive/
```

更详细的索引和跳转统一放在 [docs/README.md](docs/README.md)。
