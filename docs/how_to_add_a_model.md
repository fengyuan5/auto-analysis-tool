# How To Add A Model

这份文档的目标很直接：

让后来的人看到这个仓库后，知道怎么把一个新的模型样例迁进来，而不是只看懂项目背景。

## 迁移目标

新增一个模型时，先不要追求把真实运行链路一次性全接完。先满足最小闭环：

`recipe -> baseline run -> optimized run -> profiling -> validate -> report`

## 你需要准备什么

至少准备 7 类信息或文件：

1. 样例元数据
   模型名、任务类型、模式、硬件、CANN、框架。
2. 人读文档
   `README.md`，说明模型、依赖、环境、运行方式、输出位置、优化点和验证方式。
3. 运行入口
   主入口脚本、工作目录、默认参数。
4. 依赖声明
   `requirements.txt`、`environment.yml` 或 `Dockerfile` 之一。
5. 两次运行结果
   一次 baseline，一次 optimized。
6. 两份 profiling 摘要
   每次运行各一份，哪怕暂时只是人工抽取后的简化版本。
7. 如果有独立配置
   放在 `config/` 或 `configs/`。

## 操作步骤

### 1. 选一个参考样例

从现有 3 个样例里选最接近你的场景的那个：

1. `hunyuan_video`
   更接近推理 + profiling 挂接。
2. `qwen2_5_rl_demo`
   更接近训练 + checkpoint/收益。
3. `pi0_infer_with_torch`
   更接近外部依赖 + benchmark。

## 2. 复制模板

至少复制下面这些模板或对照现有示例补齐：

1. [recipe 模板](../examples/templates/recipe.yaml)
2. [run 模板](../examples/templates/run.json)
3. [profiling 模板](../examples/templates/profiling.json)
4. [README 模板](../examples/templates/RECIPE_README.md)
5. [run.sh 模板](../examples/templates/run.sh)
6. [requirements.txt 模板](../examples/templates/requirements.txt)

目标目录约定：

1. `examples/recipes/<recipe_name>/recipe.yaml`
2. `examples/recipes/<recipe_name>/README.md`
3. `examples/recipes/<recipe_name>/run.sh` 或 `run.py`
4. `examples/recipes/<recipe_name>/requirements.txt` / `environment.yml` / `Dockerfile`
5. `examples/runs/<run_id>.json`
6. `examples/profiling/<run_id>.json`

## 3. 填 `recipe.yaml`

优先填对这些字段：

1. `recipe_name`
2. `model_name`
3. `task_type`
4. `mode`
5. `domain`
6. `entrypoint`
7. `baseline_run_id`
8. `optimized_run_id`

注意：

1. `mode` 目前只接受 `infer`、`train`、`train_infer`
2. `domain` 目前只接受 `llm`、`multimodal`、`spatial_intelligence`、`embodied_intelligence`、`recsys`、`other`
3. `entrypoint.type` 目前只接受 `shell` 或 `python`

## 4. 补 `README.md`

这是合入规则里的强制文件，不是可选项。

至少写清下面内容：

1. 模型和任务是什么
2. 依赖和环境是什么
3. 怎么快速运行
4. 输出结果在哪里
5. 做了哪些优化
6. 用什么方式验证

## 5. 补统一入口和依赖文件

这两类文件也是后续接入统一数据库和 agent 的重要前提。

至少满足：

1. 有 `run.sh` 或 `run.py`
2. 在 `recipe.yaml` 里声明主入口
3. 有 `requirements.txt`、`environment.yml` 或 `Dockerfile` 之一
4. 如果依赖外部仓、权重、数据集，也要在 `recipe.yaml` 里结构化写清楚

## 6. 填两份 `run.json`

至少保证 baseline 和 optimized 各有一份记录。

建议至少填：

1. `run_id`
2. `recipe_name`
3. `variant`
4. `status`
5. `run_mode`
6. `device_count`
7. `latency_ms` 或 `throughput`
8. `memory_peak_gb`
9. 精度或收益指标

## 7. 填两份 `profiling.json`

如果暂时没有完整 profiling 文件，也不要卡住。先抽最小摘要字段：

1. `host_wait_ratio`
2. `kernel_utilization`
3. `io_wait_ratio`
4. `launch_overhead_ms`
5. `dominant_issue`

这一步的目的不是追求完美，而是先让自动分析链路能给出统一输出。

## 8. 运行校验

```bash
PYTHONPATH=src python3 -m auto_analysis_tool validate
```

通过标准：

1. recipe 必填字段齐全
2. 枚举值合法
3. `baseline_run_id` 和 `optimized_run_id` 对应的 `run.json` 存在
4. 对应的 `profiling.json` 存在
5. 人工补齐 `README.md`、统一入口和依赖文件

## 9. 生成报告

```bash
PYTHONPATH=src python3 -m auto_analysis_tool report
```

你要检查的不是报告有没有“绝对正确”，而是它有没有做到：

1. 能统一展示模型信息
2. 能统一展示 baseline 和 optimized 差异
3. 能基于 profiling 产出可读建议

## 10. 什么时候算迁移完成

满足下面 5 点，就算完成了第一版迁移：

1. 新模型能被 `discover` 发现
2. `validate` 通过
3. `report` 能输出这个模型的分析摘要
4. 样例目录里有 `README.md`、统一入口和依赖文件
5. 其他人能照着你的样例继续接入同类模型

## 常见问题

### 没有真实 profiling 怎么办

先填简化版 `profiling.json`。这个仓库当前的重点是统一数据闭环，不是强制接入真实平台采集。

### 训练样例没有 latency 怎么办

可以只填 `throughput`、`memory_peak_gb` 和训练收益指标，例如 `reward_score`。

### 现在为什么还是 mock 数据

因为这个仓库当前承担的是迁移参考和结构收敛角色。真实 adapter 是下一阶段，但 schema、模板和校验应该先稳定下来。
