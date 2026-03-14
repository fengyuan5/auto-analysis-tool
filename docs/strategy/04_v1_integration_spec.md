# V1 接入规范

## 1. 目标

V1 不是为了把所有 recipe 一次性做成统一标准，而是为了让它们先接入最小闭环。

V1 只要求五件事：

1. 能识别样例是什么。
2. 能知道怎么运行。
3. 能知道依赖什么。
4. 能知道结果落到哪里，以及平台如何挂接 profiling 采集。
5. 能知道优化前后怎么比较。

---

## 2. recipe 接入规范

### 2.1 一个样例至少要提供什么

每个样例至少要提供五类信息：

1. 样例元数据。
   样例名称、模型名称、任务类型、推理/训练、目标硬件、目标 CANN 版本、依赖框架。
2. 运行信息。
   主入口脚本或主入口命令、单卡/多卡运行方式、关键环境变量、最小可运行配置。
3. 外部依赖信息。
   外部代码仓、模型权重来源、数据集来源、是否依赖 Docker、是否依赖 Git LFS。
4. 结果信息。
   日志路径、结果文件路径、checkpoint 路径。
5. 验证信息。
   主要性能指标、主要精度指标、优化前后比较口径。
6. 采集提示信息。
   是否支持 profiling、平台如何挂接 profiling、适用于哪种运行模式。

### 2.2 V1 对 recipe 的最低要求

V1 不要求所有 recipe 完全一致，但至少要满足：

1. 有 README。
2. 有明确入口。
3. 有最小可运行说明。
4. 有结果输出位置说明。
5. 如果支持 profiling，要说明平台如何挂接 profiling 采集。

### 2.3 平台侧需要补什么

V1 阶段，平台侧应补一层适配：

1. 样例发现。
2. 外部依赖登记。
3. 运行描述标准化。
4. 结果收集。
5. 差异比对。

---

## 3. 数据底座最小字段集

V1 先定义五类对象：

1. 样例对象。
2. 运行对象。
3. 结果对象。
4. 结论对象。
5. 验证对象。

### 3.1 样例对象

建议字段：

1. `repo_name`
2. `example_name`
3. `model_name`
4. `task_type`
5. `mode`
6. `framework`
7. `hardware_target`
8. `cann_version`
9. `readme_path`
10. `entry_command`
11. `entry_script`
12. `external_dependencies`

作用：

描述“这是什么样例，怎么启动，依赖什么”。

### 3.2 运行对象

建议字段：

1. `run_id`
2. `example_name`
3. `run_mode`
4. `device_count`
5. `env_summary`
6. `input_config`
7. `weight_source`
8. `dataset_source`
9. `start_time`
10. `end_time`
11. `status`

作用：

描述“这次怎么跑的，跑没跑成功”。

### 3.3 结果对象

建议字段：

1. `run_id`
2. `log_path`
3. `artifact_path`
4. `checkpoint_path`
5. `profiling_path`
6. `latency`
7. `throughput`
8. `memory_peak`
9. `accuracy_metric`
10. `custom_metrics`

作用：

描述“跑出了什么结果”。其中 `profiling_path` 对应平台内部数据生产产物，不要求 recipe 直接对外呈现。

### 3.4 结论对象

建议字段：

1. `analysis_id`
2. `run_id`
3. `analysis_type`
4. `problem_summary`
5. `evidence_summary`
6. `recommendation`
7. `expected_gain`
8. `confidence`

作用：

描述“工具给了什么结论”。

### 3.5 验证对象

建议字段：

1. `validation_id`
2. `baseline_run_id`
3. `optimized_run_id`
4. `change_summary`
5. `metric_diff`
6. `is_effective`
7. `risk_note`

作用：

描述“建议做完之后有没有真的变好”。

---

## 4. V1 做完后应该达到什么状态

V1 做完后，平台至少要做到：

1. 能把 recipe 样例统一登记起来。
2. 能按统一方式拉起任务。
3. 能统一收集结果。
4. 能在样例之间做最基本的横向比较。
5. 能支撑第一版自动分析和优化验证闭环。
