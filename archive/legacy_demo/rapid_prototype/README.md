# Auto Analysis Tool Demo

这个 demo 把当前“文档项目”收敛成一个最小可运行的新项目骨架，目标不是直接拉起真实 Ascend 任务，而是先证明三件事：

1. 可以把选定 recipe 统一登记。
2. 可以把运行结果和 profiling 统一结构化。
3. 可以从统一数据里产出面向单模型优化的分析报告，并给出项目改造路径。

## 这次 demo 选的模型

首批只放 3 个样例，对应当前分析里最明确、最适合做最小闭环的试点：

1. `hunyuan_video`
2. `qwen2_5_rl_demo`
3. `pi0_infer_with_torch`

这 3 个样例分别覆盖：

1. 推理 + profiling 挂接
2. 训练 + 日志/checkpoint/收益分析
3. 具身智能推理 + 外部依赖接入

## 当前 project 到新 project 的改造思路

当前 repo 主要是：

1. 目标和闭环说明
2. recipe 盘点
3. V1 规范

它的问题不是分析不够，而是还没有代码化落地。新 project 建议改成下面结构：

1. `recipes/`
   放样例元数据和接入描述。
2. `adapters/`
   把不同 recipe 的运行方式适配成统一接口。
3. `runs/`
   放每次运行的结构化记录。
4. `analysis/`
   放 profiling 规则、对比逻辑和建议生成逻辑。
5. `reports/`
   产出 Markdown/JSON 报告。

这个 demo 对应的是上面结构的最小压缩版：

1. `demo/data/recipes/`
2. `demo/data/runs/`
3. `demo/data/profiling/`
4. `demo/app/`

## 运行方式

```bash
python3 demo/main.py discover
python3 demo/main.py report
python3 demo/main.py migration
```

## 你会看到什么

1. `discover`
   展示统一登记后的 recipe 列表。
2. `report`
   展示每个样例的基线、优化后收益、profiling 发现和建议。
3. `migration`
   展示从当前文档型 project 迁移到新 project 的分阶段方案。
