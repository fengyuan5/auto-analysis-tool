# recipe 盘点结论

## 1. 第一轮结论

这 4 个 `cann-recipes-*` 仓已经具备较强的样例基础，可以直接作为第一阶段输入源。

但从平台接入视角看，它们还不是“可直接批量接入的标准资产”，而是“可用样例库 + 待统一规范的输入源”。

---

## 2. 第一批建议试点

优先选这些样例进入最小闭环试点：

1. `cann-recipes-infer/models/hunyuan-video`
   原因：入口清楚，优化点明确，支持单卡/多卡，适合做推理侧样例。
2. `cann-recipes-train/llm_rl/qwen2_5/verl_npu_demo`
   原因：单卡 A2 可跑，训练门槛低，适合做训练侧最小闭环。
3. `cann-recipes-spatial-intelligence/models/Hunyuan3D`
   原因：入口清楚，优化点清楚，空间智能场景代表性强。
4. `cann-recipes-spatial-intelligence/models/vggt`
   原因：既有推理入口，也有评测脚本，适合做“推理 + 精度验证”样例。
5. `cann-recipes-spatial-intelligence/algorithms/gaussian_splatting`
   原因：有完整训推脚本，适合算法级样例。
6. `cann-recipes-embodied-intelligence/manipulation/pi0/infer_with_torch`
   原因：对外展示价值高，入口明确，适合具身智能推理样例。

---

## 3. 第二批建议试点

第二批再考虑这些高价值但接入成本更高的样例：

1. `cann-recipes-infer/models/deepseek-r1`
2. `cann-recipes-embodied-intelligence/manipulation/pi05/train`
3. `cann-recipes-embodied-intelligence/manipulation/openvla/infer_with_om`

这些样例的问题不是价值低，而是：

1. 依赖更多外部仓和转换流程。
2. 运行链路更长。
3. 验证口径更难统一。

---

## 4. 暂不作为第一批试点

下面这些样例更适合后续平台能力成熟后再接入：

1. `cann-recipes-infer/models/hstu`
   外部依赖和算子编译较重。
2. `cann-recipes-train/llm_rl/deepseek`
   128 卡 A3 门槛高。
3. `cann-recipes-train/llm_pretrain/deepseekv32`
   64 卡 A3 门槛高，数据和权重规模大。

---

## 5. 第一轮看到的共性缺口

共性缺口主要有五类：

1. 缺统一元数据。
   模型名、任务类型、硬件、CANN 版本、输入规格没有统一结构。
2. 缺统一运行入口。
   有的用 `bash`，有的用 `python`，有的还依赖外部仓复制和 patch。
3. 缺统一 profiling 挂接方式。
   很多样例提到性能优化，但平台如何挂接 profiling、如何统一采集，还没有统一约定。
4. 缺统一优化记录。
   优化点写在 README 里比较多，但不容易结构化沉淀。
5. 缺统一验证口径。
   优化前后输入规模、环境、模型版本的可比性需要平台侧补齐。

---

## 6. 第一批 3 个详细样例

### 6.1 HunyuanVideo

状态：

1. README 完整。
2. 入口脚本明确。
3. 单卡、多卡都给了标准脚本。
4. 已经显式支持 profiling。
5. 优化点清楚，适合做推理侧高价值样例。

主要入口：

1. `scripts/test.sh`
2. `scripts/test_sp.sh`
3. `sample_video.py`

主要结果路径：

1. `./results`
2. `./results/logs`

主要缺口：

1. 缺统一元数据文件。
2. 缺统一运行描述。
3. 缺统一 profiling 挂接约定。

结论：

`HunyuanVideo` 应该作为第一批试点样例，用来验证“推理 + profiling 挂接采集”。

### 6.2 Qwen2.5 RL Demo

状态：

1. README 完整。
2. 启动脚本明确。
3. 单机训练门槛相对低。
4. 有日志、checkpoint 和评测说明。
5. 很适合做训练侧最小闭环。

主要入口：

1. `run_qwen2_5_1_5b.sh`

主要结果路径：

1. `./run_log/qwen2_5_1_5b_math.log`
2. `verl/checkpoints/...`
3. TensorBoard / SwanLab 日志

主要缺口：

1. 缺标准 profiling 采集入口。
2. 缺统一数据和权重准备方式。
3. 缺统一训练结果结构化记录方式。
4. 缺“训练配置 -> 结果 -> 收益”的统一抽象。

结论：

`Qwen2.5 RL Demo` 应该作为第一批训练侧试点，用来验证“训练 + 日志/checkpoint/收益分析”。

### 6.3 Pi0 infer_with_torch

状态：

1. 对外展示价值高。
2. 入口脚本明确。
3. 有自动下载代码、数据和模型的脚本。
4. 已经在脚本中显式做了 warmup 和 benchmark。
5. 有延迟结果输出。

主要入口：

1. `download_code_and_data.sh`
2. `run_pi0_inference.sh`
3. `test_pi0_on_ascend.py`

主要结果信号：

1. warmup 次数
2. benchmark 次数
3. 平均时延
4. 动作序列结果形状

主要缺口：

1. 缺显式 profiling 采集。
2. 缺统一结果落盘。
3. 缺统一环境快照记录。
4. 缺结构化的精度验证结果记录。

结论：

`Pi0 infer_with_torch` 应该作为第一批具身智能试点，用来验证“benchmark + 外部依赖接入”。

---

## 7. 对平台侧的直接启发

第一版平台不应该要求 recipe 先完全标准化，而应该先提供一层“接入适配层”。

这层适配至少要解决：

1. 识别样例入口。
2. 记录环境和依赖。
3. 挂接 profiling 采集。
4. 统一结果入库。
5. 统一记录优化前后差异。

---

## 8. 下一步建议

下一步直接做两件事：

1. 基于第一批样例，写第一版 recipe 接入规范。
2. 基于第一批样例，定义数据底座的最小字段集。
