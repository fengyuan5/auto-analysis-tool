# Data Contract

这份文档回答一个关键问题：

如果后续要一起共建统一数据库，并在其上开发 agent，应该以哪套 schema 为准。

## 结论

当前仓库有两层 schema 语义：

1. 目标契约
   以 [V1 接入规范](strategy/04_v1_integration_spec.md) 为准。
2. 当前可执行契约
   以 [src/auto_analysis_tool/models.py](../src/auto_analysis_tool/models.py)、
   [src/auto_analysis_tool/repository.py](../src/auto_analysis_tool/repository.py)、
   [src/auto_analysis_tool/validators.py](../src/auto_analysis_tool/validators.py) 为准。

一句话说：

策略文档定义“我们最终想沉淀成什么数据库对象”，代码定义“当前仓库已经实际跑起来的最小字段集”。

## 当前对象分层

### 1. Recipe

对应：

1. 策略层：样例对象
2. 代码层：`Recipe`

作用：

描述一个样例是什么、怎么运行、依赖什么、输出在哪里。

当前代码字段见：

[src/auto_analysis_tool/models.py](../src/auto_analysis_tool/models.py)

### 2. RunRecord

对应：

1. 策略层：运行对象 + 部分结果对象
2. 代码层：`RunRecord`

作用：

描述一次 baseline 或 optimized 运行是怎么跑的，以及产出了哪些核心结果。

说明：

当前代码里把“运行对象”和“结果对象”的最小字段压在了一起，方便先跑通 demo 闭环。后续如果数据库继续扩展，可以再拆层。

### 3. ProfilingRecord

对应：

1. 策略层：结果对象中的 profiling 相关部分
2. 代码层：`ProfilingRecord`

作用：

描述一次运行中最关键的 profiling 摘要信号。

### 4. RecipeAnalysis

对应：

1. 策略层：结论对象 + 验证对象
2. 代码层：`RecipeAnalysis`、`Finding`、`ValidationDiff`

作用：

描述一次分析输出了什么问题、建议和验证结果。

## Source Of Truth

不同角色建议按下面方式使用：

### 1. 设计原则讨论

以 [V1 接入规范](strategy/04_v1_integration_spec.md) 和 [recipe 合入规则](strategy/05_recipe_admission_rules.md) 为准。

### 2. 当前仓库接入和示例运行

以代码里的 dataclass、repository 和 validate 行为为准。

### 3. 数据库和 agent 共建

建议遵循一个原则：

1. 新字段设计先参考策略文档中的对象分类
2. 当前实现必须同时在代码 schema 和 `validate` 里落地
3. 新增字段要确保能被 recipe、run、profiling、analysis 串起来

## 当前最小数据库闭环

当前仓库实际已经跑通的是：

`recipe.yaml -> run.json -> profiling.json -> validate -> report`

对数据库和 agent 共建来说，这意味着当前最稳的起点不是直接做复杂推理，而是先保证：

1. recipe 元数据稳定
2. run 记录稳定
3. profiling 摘要稳定
4. 分析输出可以稳定回连到 baseline/optimized

## 后续扩展原则

如果未来要继续扩 schema，优先顺序建议是：

1. 补环境快照和输入配置
2. 补外部依赖和权重来源
3. 补训练收益字段
4. 补更细 profiling 指标
5. 补跨模型聚合标签

只要继续沿着这个方向扩，数据库和上层 agent 的接口就不会失控。
