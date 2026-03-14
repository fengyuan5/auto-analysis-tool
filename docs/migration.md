# Migration

## 当前项目是什么

当前项目已经把下面内容讲清楚了：

1. 为什么要做闭环分析工具
2. 第一批试点 recipe 应该选谁
3. V1 接入规范和合入规则应该长什么样

对应文档已经统一收进 [docs/strategy](/Users/fengyuannfoxmail.com/Projects/auto-analysis-tool/docs/strategy/README.md)。

当前缺的不是思路，而是代码化落地。

## 新项目应该怎么分层

建议按下面结构演进：

1. `recipes/`
   统一样例资产。
2. `adapters/`
   把不同 recipe 仓接成统一运行接口。
3. `runs/`
   落每次运行的结构化信息。
4. `profiling/`
   统一管理平台采集结果。
5. `analysis/`
   放规则、打标、建议和验证逻辑。
6. `reports/`
   面向外部和内部输出。

## 分阶段推进

### Phase 1

先把 mock 数据跑通，证明 schema、report 和验证链路是对的。

### Phase 2

把 `hunyuan_video`、`qwen2_5_rl_demo`、`pi0_infer_with_torch` 接到真实 adapter。

### Phase 3

加入跨 recipe 聚合分析，把单模型问题提升成 CANN 和芯片输入。

## 对未来迁移的直接意义

这个仓库未来要承担的角色不是“再解释一遍为什么要迁移”，而是“给后来者一个照着做的样板”。

因此迁移时最应该优先复用的是：

1. [新增模型操作手册](/Users/fengyuannfoxmail.com/Projects/auto-analysis-tool/docs/how_to_add_a_model.md)
2. [recipe 模板](/Users/fengyuannfoxmail.com/Projects/auto-analysis-tool/examples/templates/recipe.yaml)
3. `validate` 命令
4. 现有 3 个示例 recipe
