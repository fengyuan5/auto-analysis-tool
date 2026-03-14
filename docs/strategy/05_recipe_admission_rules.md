# recipe 样例合入规则 V1

## 1. 目的

这套规则用于约束内部和外部合入的 recipe 样例，目标不是限制样例创新，而是保证样例可以被统一抽取、统一运行、统一入库。

有了这套规则，后续才能稳定支撑：

1. 统一数据库构建。
2. 模型优化 agent。
3. bound 搜索 agent。
4. 芯片建议 agent。
5. profiling 分析 agent。
6. 其他基于数据库的自动分析能力。

一句话说：

合入规则的目标，是把“能跑的样例”变成“能被平台理解和复用的样例”。

---

## 2. 基于现状看到的问题

从现有 `cann-recipes-*` 样例来看，已经有很多高价值内容，但如果要支撑统一数据库和 agent，主要有五类问题：

1. 元数据不统一。
   模型名、任务类型、硬件、CANN 版本、依赖框架分散在 README 里。
2. 运行入口不统一。
   有的用 `bash`，有的用 `python`，有的还依赖外部仓复制、patch 或下载脚本。
3. 外部依赖不透明。
   上游仓、权重、数据集、Docker、Git LFS 等依赖没有统一声明。
4. profiling 挂接方式不统一。
   哪些样例支持 profiling、如何开启、平台怎么挂接，没有统一声明。
5. 优化记录和验证口径不统一。
   很多样例有优化说明，但不便于结构化提取和横向比较。

所以，V1 合入规则必须优先解决“可抽取、可运行、可比较”。

---

## 3. 合入规则的总体原则

所有新样例合入时，必须满足四个原则：

1. 可识别。
   平台能自动识别这个样例是什么。
2. 可拉起。
   平台能知道如何运行这个样例。
3. 可采集。
   平台能知道日志、结果去哪里拿，以及 profiling 如何挂接采集。
4. 可比较。
   平台能知道优化前后如何做统一对比。

如果一个样例只满足“能跑”，但不满足上面四点，就不应直接作为标准 recipe 合入。

---

## 4. 合入样例必须提供的文件

每个样例目录至少要提供下面 6 类文件。

### 4.1 `recipe.yaml`

这是强制文件，用于统一元数据和运行描述。

没有这个文件，不进入标准 recipe 样例。

### 4.2 `README.md`

这是强制文件，用于人读。

要求：

1. 说明模型和任务是什么。
2. 说明依赖和环境。
3. 说明如何快速运行。
4. 说明输出结果在哪里。
5. 说明优化点和验证方式。

### 4.3 统一入口脚本

至少要有一个标准入口：

1. `run.sh`
   或
2. `run.py`

如果同时有单卡、多卡、训练、推理多种入口，也必须在 `recipe.yaml` 中声明主入口和变体入口。

### 4.4 依赖文件

至少要有一种依赖声明：

1. `requirements.txt`
2. `environment.yml`
3. `Dockerfile`

如果依赖外部仓、模型权重、数据集，也必须在 `recipe.yaml` 中单独声明，不能只写在 README 里。

### 4.5 配置文件

如果样例依赖 YAML/JSON/命令行参数配置，配置文件必须放在固定目录，例如：

1. `config/`
2. `configs/`

不能把关键参数散在多个脚本里无法追踪。

### 4.6 可选补充文件

如样例支持 profiling、评测或优化记录，建议补：

1. `profiling.yaml`
2. `metrics.yaml`
3. `CHANGELOG_OPT.md`

V1 不强制，但建议逐步收敛。

---

## 5. `recipe.yaml` 必填字段

`recipe.yaml` 是整个规则的核心。V1 先要求下面字段必须有。

### 5.1 基本信息

1. `recipe_name`
2. `model_name`
3. `task_type`
4. `mode`
   infer / train / train_infer
5. `domain`
   llm / multimodal / spatial_intelligence / embodied_intelligence / recsys / other

### 5.2 环境信息

1. `hardware_target`
2. `cann_version`
3. `framework`
4. `python_version`

### 5.3 入口信息

1. `entrypoint.type`
   shell / python
2. `entrypoint.path`
3. `entrypoint.workdir`
4. `entrypoint.default_args`

### 5.4 外部依赖信息

1. `upstream_repos`
2. `model_weights`
3. `datasets`
4. `container`
5. `requires_git_lfs`

### 5.5 输出信息

1. `outputs.log_dir`
2. `outputs.result_dir`
3. `outputs.checkpoint_dir`

### 5.6 profiling 挂接信息

1. `profiling.supported`
2. `profiling.enable_mode`
3. `profiling.enable_flag`
4. `profiling.notes`

### 5.7 验证信息

1. `metrics.performance`
2. `metrics.accuracy`
3. `comparison_baseline`

---

## 6. 目录和产物规则

为了统一信息抽取，样例目录和产物路径必须尽量稳定。

### 6.1 目录建议

样例目录建议统一为：

1. `README.md`
2. `recipe.yaml`
3. `run.sh` 或 `run.py`
4. `requirements.txt` / `Dockerfile`
5. `config/`
6. `scripts/`
7. `tools/`

### 6.2 运行产物路径

统一约定：

1. 日志默认放 `outputs/logs/`
2. 结果文件默认放 `outputs/results/`
3. checkpoint 默认放 `outputs/checkpoints/`

V1 允许兼容旧样例的历史路径，但新合入样例必须尽量遵守这个约定。

说明：

profiling 不作为 recipe 必须直接呈现的对外产物。profiling 文件由平台在内部数据生产阶段采集和管理，不强制要求 recipe 自己暴露固定 profiling 目录。

### 6.3 命名规则

每次运行建议带唯一 run id，至少体现在产物目录中，例如：

1. `outputs/logs/<run_id>/`
2. `outputs/results/<run_id>/`

这样后续数据库才能稳定关联一次运行。

---

## 7. profiling 规则

profiling 作为平台内部数据生产内容，不要求 recipe 把 profiling 文件直接作为标准对外产物提供。

如果样例支持 profiling，recipe 只需要明确三件事：

1. 如何开启 profiling。
2. 平台从哪个入口挂接 profiling。
3. profiling 适用于哪种运行模式。

V1 最低要求：

1. 在 `recipe.yaml` 中声明 profiling 开关方式。
2. 在 `recipe.yaml` 中声明 profiling 适用模式。
3. README 中给出 profiling 使用说明。

如果样例暂时不支持 profiling，也必须显式写：

1. `profiling.supported: false`

不能留空。

---

## 8. 优化记录和验证规则

样例如果号称“做了优化”，就必须至少能回答下面问题：

1. 优化了什么。
2. 基于什么现象做的优化。
3. 带来了什么收益。
4. 用什么口径验证。

V1 最低要求：

1. README 中必须有“优化点”小节。
2. README 中必须有“验证方式”小节。
3. `recipe.yaml` 中必须声明主要性能指标和精度指标。

后续平台才能把这些信息抽成结构化知识，而不是只保留自然语言描述。

---

## 9. 外部依赖规则

外部依赖必须结构化声明，不能只在 README 里写一句“依赖某某仓”。

### 9.1 必须声明的外部依赖

1. 上游代码仓。
2. 权重来源。
3. 数据集来源。
4. 特殊安装方式。
5. 是否依赖网络下载。

### 9.2 对外部依赖的要求

如果样例依赖外部内容，必须尽量满足：

1. 给出固定版本或 commit。
2. 给出下载路径。
3. 给出本地落盘位置。
4. 给出失败时的替代方式。

否则平台很难稳定复现。

---

## 10. 合入门槛

V1 建议把合入门槛分成三级。

### 10.1 Level 1：可展示样例

要求：

1. 有 README。
2. 有入口。
3. 能手工跑通。

这种样例可以存在，但不进入统一数据库主流程。

### 10.2 Level 2：可接入样例

要求：

1. 满足 README + `recipe.yaml` + 统一入口。
2. 外部依赖明确。
3. 输出路径明确。

这种样例可以进入统一数据库。

### 10.3 Level 3：可闭环样例

要求：

1. 满足 Level 2。
2. 支持 profiling 或 benchmark 标准采集。
3. 支持优化前后可比验证。

这种样例可以进入自动分析闭环和 agent 流程。

V1 目标是尽快把现有高价值样例拉到 Level 2，第一批试点样例拉到 Level 3。

---

## 11. 合入检查清单

新样例合入时，至少检查下面 10 项：

1. 是否有 `recipe.yaml`
2. 是否有 `README.md`
3. 是否有明确入口
4. 是否声明硬件和 CANN 版本
5. 是否声明外部仓、权重、数据集
6. 是否声明日志和结果路径
7. 是否声明 profiling 支持情况
8. 是否声明主要指标
9. 是否说明优化点
10. 是否说明验证方式

通过这 10 项，才进入标准 recipe 样例。

---

## 12. 推荐的 `recipe.yaml` 示例

```yaml
recipe_name: hunyuan-video
model_name: HunyuanVideo
task_type: text_to_video_inference
mode: infer
domain: multimodal

hardware_target: Atlas A2
cann_version: 8.5.0.alpha002
framework: torch
python_version: "3.11"

entrypoint:
  type: shell
  path: scripts/test.sh
  workdir: .
  default_args: []

upstream_repos:
  - name: HunyuanVideo
    url: https://github.com/Tencent-Hunyuan/HunyuanVideo
    required: true

model_weights:
  - name: HunyuanVideo
    source: huggingface
    required: true
    local_path: ckpts/

datasets: []

container:
  required: false

requires_git_lfs: false

outputs:
  log_dir: outputs/logs/
  result_dir: outputs/results/
  checkpoint_dir: ""

profiling:
  supported: true
  enable_mode: single
  enable_flag: --prof-dit
  notes: platform_collects_in_internal_data_pipeline

metrics:
  performance:
    - latency
    - throughput
  accuracy: []

comparison_baseline:
  type: previous_run
```

---

## 13. 当前规则的作用边界

这版规则只解决一件事：

让 recipe 样例可被统一抽取、统一运行、统一入库。

它还不负责：

1. 自动完成所有依赖安装。
2. 自动修复所有历史样例。
3. 自动保证所有样例都可一键运行。

V1 的重点是先把“可平台化接入”的门槛定义清楚。
