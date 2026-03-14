# Auto Analysis Tool

面向昇腾/CANN 生态的模型分析与优化原型项目。

这个仓库的目标，不是单纯收集一些 recipe，也不是只做一次性的 profiling 分析。

它要做的是三件事：

1. 把不同来源的 recipe 样例统一抽取、统一运行、统一入库。
2. 建立可持续演进的统一数据库。
3. 基于这套数据库，支撑上层若干 agent 的建设和迭代。

当前已经明确的上层能力包括：

1. 统一数据库构建
2. 模型优化 agent
3. bound 搜索 agent
4. 芯片建议 agent
5. profiling 分析 agent
6. 其他基于数据库的自动分析能力

一句话说，这个仓库要解决的是：

把“分散、能跑但难复用的 recipe 样例”，逐步变成“可被平台理解、可被数据库吸收、可被 agent 消费的标准资产”。

这个仓库现在分成两层内容：

1. `docs/strategy/`
   负责沉淀目标、闭环、试点样例和接入规范。
2. `src/auto_analysis_tool/` 与 `examples/`
   负责把这些分析落成一个可运行、可测试、可继续扩展的完整项目骨架。

## 项目目标

项目聚焦一条最小闭环：

`recipe -> run -> profiling -> analysis -> validation -> report`

第一版先证明三件事：

1. 选定 recipe 可以被统一登记和发现。
2. 运行结果与 profiling 可以进入统一数据结构。
3. 系统可以自动生成单模型优化建议和验证摘要。

## 为什么要做这件事

如果没有统一数据库，后续很多工作都会停留在人工经验层：

1. recipe 信息散在 README、脚本和外部仓里，难以稳定抽取。
2. 运行入口不统一，样例之间无法形成批量接入和横向比较。
3. profiling、结果和优化记录难以结构化沉淀。
4. 单模型经验很难沉淀成可复用知识，更难支撑上层 agent。

所以这件事的核心不是“再做一批分析”，而是先把数据库底座搭起来：

`recipe -> run -> profiling -> analysis -> validation -> database -> agents`

## 为了这个目的，recipe 需要做到什么

如果 recipe 想进入统一数据库并支撑后续 agent，它至少要满足四个条件：

1. 可识别
   平台能知道它是什么模型、什么任务、什么模式、什么环境。
2. 可拉起
   平台能知道主入口是什么，怎么运行，依赖什么。
3. 可采集
   平台能知道日志、结果、checkpoint 和 profiling 如何挂接或记录。
4. 可比较
   平台能知道 baseline 和 optimized 如何对比，收益口径是什么。

进一步落到 recipe 资产本身，至少要逐步具备这些内容：

1. `recipe.yaml`
   统一元数据、入口、依赖、输出和 profiling 信息。
2. `README.md`
   给人读，讲清模型、环境、运行方式、输出位置、优化点和验证方式。
3. 统一入口
   `run.sh` 或 `run.py`，以及在 `recipe.yaml` 里的主入口声明。
4. 依赖声明
   `requirements.txt`、`environment.yml` 或 `Dockerfile`。
5. 结构化运行记录
   baseline 和 optimized 的 `run.json`。
6. 结构化 profiling 摘要
   每次运行对应的 `profiling.json`。

这也是为什么这个项目一开始就强调 recipe 合入规则，而不是只强调模型跑通。

## 当前项目已经提供了什么

围绕上面的目标，这个仓库当前已经提供了 4 类东西：

1. 设计原则和规则文档
   说明为什么要做数据库、为什么要有合入规则、V1 的最小闭环是什么。
2. 迁移操作手册和模板
   让后续同学知道新增一个模型时，具体该补什么文件、怎么跑校验。
3. 示例资产
   用 3 个代表样例演示推理、训练和具身智能场景怎么落到统一结构。
4. 最小代码骨架
   提供 `discover`、`validate`、`report` 这条最小链路，证明 schema 和闭环是可执行的。

## 当前纳入的首批样例

1. `hunyuan_video`
2. `qwen2_5_rl_demo`
3. `pi0_infer_with_torch`

这 3 个样例覆盖了推理、训练和具身智能推理三类代表路径。

## 你如果是不同角色，建议先看什么

### 1. 想理解设计原则的同学

先看：

1. [项目目标与闭环](docs/strategy/01_goals_and_closures.md)
2. [执行推进方案](docs/strategy/02_execution_plan.md)
3. [项目架构说明](docs/architecture.md)

### 2. 准备后续合入 recipe 的同学

先看：

1. [新增模型操作手册](docs/how_to_add_a_model.md)
2. [recipe 合入规则](docs/strategy/05_recipe_admission_rules.md)
3. [模板说明](examples/templates/README.md)
4. [试点 recipe 盘点](docs/strategy/03_recipe_inventory.md)

### 3. 准备一起共建数据库和后续 agent 的同学

先看：

1. [V1 接入规范](docs/strategy/04_v1_integration_spec.md)
2. [recipe 合入规则](docs/strategy/05_recipe_admission_rules.md)
3. [数据契约](docs/data_contract.md)
4. [数据模型](src/auto_analysis_tool/models.py)
5. [数据加载层](src/auto_analysis_tool/repository.py)
6. [规则校验层](src/auto_analysis_tool/validators.py)

## 仓库内容总览

### 1. 面向未来迁移的核心入口

1. [新增模型操作手册](docs/how_to_add_a_model.md)
2. [recipe 合入规则](docs/strategy/05_recipe_admission_rules.md)
3. [项目架构说明](docs/architecture.md)
4. [数据契约](docs/data_contract.md)
5. [迁移说明](docs/migration.md)

### 2. 之前的设计思路和策略文档

1. [策略文档总入口](docs/strategy/README.md)
2. [从这里开始看](docs/strategy/00_start_here.md)
3. [项目目标与闭环](docs/strategy/01_goals_and_closures.md)
4. [执行推进方案](docs/strategy/02_execution_plan.md)
5. [试点 recipe 盘点](docs/strategy/03_recipe_inventory.md)
6. [V1 接入规范](docs/strategy/04_v1_integration_spec.md)
7. [recipe 合入规则](docs/strategy/05_recipe_admission_rules.md)
8. [recipe 盘点表](docs/strategy/03_recipe_inventory.csv)

### 3. 模板和示例资产

1. [模板说明](examples/templates/README.md)
2. [recipe 模板](examples/templates/recipe.yaml)
3. [README 模板](examples/templates/RECIPE_README.md)
4. [run.sh 模板](examples/templates/run.sh)
5. [requirements.txt 模板](examples/templates/requirements.txt)
6. [run 模板](examples/templates/run.json)
7. [profiling 模板](examples/templates/profiling.json)
8. [HunyuanVideo 示例](examples/recipes/hunyuan_video/recipe.yaml)
9. [Qwen2.5 RL Demo 示例](examples/recipes/qwen2_5_rl_demo/recipe.yaml)
10. [Pi0 示例](examples/recipes/pi0_infer_with_torch/recipe.yaml)

### 4. 代码入口

1. [CLI 入口](src/auto_analysis_tool/cli.py)
2. [数据加载层](src/auto_analysis_tool/repository.py)
3. [规则校验层](src/auto_analysis_tool/validators.py)
4. [分析层](src/auto_analysis_tool/analyzer.py)
5. [报告层](src/auto_analysis_tool/reporting.py)
6. [数据模型](src/auto_analysis_tool/models.py)

### 5. 测试和 CI

1. [Repository 测试](tests/test_repository.py)
2. [CLI 测试](tests/test_cli.py)
3. [GitHub CI](.github/workflows/ci.yml)

### 6. 历史归档

1. [归档说明](archive/README.md)
2. [早期快速原型](archive/legacy_demo/rapid_prototype/README.md)

## 仓库结构

```text
.
├── README.md
├── pyproject.toml
├── src/auto_analysis_tool/
├── examples/
│   ├── recipes/
│   ├── runs/
│   └── profiling/
├── tests/
├── docs/
│   ├── README.md
│   ├── strategy/
│   ├── architecture.md
│   ├── data_contract.md
│   ├── how_to_add_a_model.md
│   └── migration.md
├── .github/workflows/
├── archive/
```

说明：

1. `src/auto_analysis_tool/`
   是可安装的 Python 包。
2. `examples/`
   是示例 recipe、run 和 profiling 数据。
3. `archive/`
   放历史原型和与主线无关的参考产物，不影响当前主路径。
4. `docs/strategy/`
   是之前设计思路和盘点文档的正式归档位置。

## 快速开始

### 1. 发现样例

```bash
PYTHONPATH=src python3 -m auto_analysis_tool discover
```

### 2. 生成分析报告

```bash
PYTHONPATH=src python3 -m auto_analysis_tool report
```

### 3. 查看迁移方案

```bash
PYTHONPATH=src python3 -m auto_analysis_tool migration
```

### 4. 校验 recipe 规范

```bash
PYTHONPATH=src python3 -m auto_analysis_tool validate
```

### 5. 运行测试

```bash
python3 -m unittest discover -s tests
```

## 新增一个模型时怎么做

如果这个仓库要作为未来迁移参考，最重要的入口不是命令，而是接入步骤。直接看：

1. [新增模型操作手册](docs/how_to_add_a_model.md)
2. [recipe 合入规则](docs/strategy/05_recipe_admission_rules.md)
3. [recipe 模板](examples/templates/recipe.yaml)
4. [README 模板](examples/templates/RECIPE_README.md)
5. [run.sh 模板](examples/templates/run.sh)
6. [requirements.txt 模板](examples/templates/requirements.txt)
7. [run 模板](examples/templates/run.json)
8. [profiling 模板](examples/templates/profiling.json)

## 为什么 `recipe.yaml` 用 JSON 形式

示例里的 `recipe.yaml` 使用了 JSON-compatible YAML 写法，这样可以先保持零第三方依赖，同时保留后续切换到标准 YAML 解析器的空间。

## 文档入口

1. [文档导航](docs/README.md)
2. [策略文档入口](docs/strategy/00_start_here.md)
3. [新增模型操作手册](docs/how_to_add_a_model.md)
4. [数据契约](docs/data_contract.md)
5. [项目架构说明](docs/architecture.md)
6. [从当前项目到新项目的迁移说明](docs/migration.md)
