# 测试驱动的 Python 函数修复助手

用于课题 07：研究公开 pytest 失败反馈是否帮助模型真正修复短小纯函数。系统由任务、模型调用、Docker 执行、三组控制、独立隐藏评分、日志与报告六部分组成。

## 固定范围

- 保留冻结的 **50 道 HumanEvalPack 正式题**，默认每题每策略运行一轮，共 **150 个 run**。
- 保留 3 道演示题、共 30 个测试函数，覆盖空输入、重复元素、边界和索引问题。
- 保留 **DeepSeek API 和 MLX-LM 本地模型适配器**。
- 三组使用相同模型、题目和停止条件，A/B/C 总提交上限为 **1/3/3**，最多 350 次模型调用；不是三次额外重试。

| 策略 | 总提交上限 | 模型是否看到详细失败诊断 |
| --- | ---: | --- |
| single-shot | 1 | 无后续修复 |
| retry-without-feedback | 3 | 否；公开失败后只要求重新生成 |
| test-feedback | 3 | 是；提供上一轮公开 pytest 输出 |

模型只能通过 `submit_solution(content)` 提交完整 solution.py，没有 shell 或其他文件工具。B/C 公开通过即停止。隐藏结果不反馈给模型。

## 本机运行环境

固定使用 Linux/WSL Ubuntu、Python 3.12+ 和 Docker。已有本机环境可直接使用项目 `.venv`；从新环境安装时执行：

```bash
python3.12 -m venv .venv
.venv/bin/pip install -e '.[dev]'
make sandbox-build
.venv/bin/repair-agent doctor
make check
make sandbox-test
```

Docker Desktop/Engine 在测试和实验期间保持运行。主控制器调用模型 API，候选代码只在断网、资源受限、根文件系统及 workspace 只读的 Docker 中执行。密钥、个人目录和原始题库不会挂载给候选代码；隐藏测试只在修复结束后的评测容器挂载。

已有 `.env` 时保留它；首次配置可复制 `.env.example`，自行填写密钥，不在聊天或日志中公开。

```text
DEEPSEEK_API_KEY=在本地填写
REPAIR_ASSISTANT_PROVIDER=deepseek
REPAIR_ASSISTANT_MODEL=deepseek-flash
```

MLX-LM 服务已启动时可改用：

```text
REPAIR_ASSISTANT_PROVIDER=mlx-local
REPAIR_ASSISTANT_MODEL=default_model
REPAIR_ASSISTANT_BASE_URL=http://127.0.0.1:8080/v1
REPAIR_ASSISTANT_MODEL_TIMEOUT_SECONDS=600
REPAIR_ASSISTANT_MAX_TOKENS=2048
```

本地适配器接收完整 Python 源码并转换为同一提交接口；不会赋予模型代码执行权限。

## 从演示到正式实验

```bash
# 三道演示题，三组一轮，共 9 个 run
make experiment TASKS_DIR=benchmarks/tasks

# 默认：50 道正式题，三组一轮，共 150 个 run
make experiment

# 单题调试
.venv/bin/repair-agent run benchmarks/tasks/chunk-list --strategy test-feedback
```

测试和正式实验会调用已配置的模型并产生实际费用。重复实验是可选扩展，需显式设置 `REPETITIONS=3`；默认一轮即可，不自动增加预算。

## 日志、评分与简洁报告

每轮保存代码、模型请求/响应和公开反馈，使用普通 JSONL 日志。公开测试仍有只读保护与文件校验；去掉日志哈希链不影响测试保护。

修复完全停止后，独立评分首次/最终公开和隐藏测试；原始错误函数只做一次轻量隐藏评分，用于检查原本正确的测试函数是否被改坏。回归按现有 pytest 测试函数的 passed→failed 统计，没有运行时逐断言追踪或自动拆分工具。50 道题现有测试保持冻结，来源和版本元数据保留。

```text
results/experiments/20261031_001/
  config.json             基本实验配置
  results.jsonl           每个 run 结束后立即保存的结果
  report.json             机器可读汇总
  raw-runs.csv            原始逐 run 数据
  strategy-metrics.csv    三组汇总
  test-results.csv        隐藏测试函数的结果变化
  report.md               唯一的课程报告，含人工错误分析区
  figures/*.svg           四张图：隐藏成功率、公隐差距、可靠性、调用与耗时
  runs/group_a/20261031_001_001/   A组任务；题目和策略见 summary.json
    events.jsonl          普通过程日志、模型响应、公开测试诊断
    summary.json          首次/最终结果、回归、超时、实际用量与耗时
    original_code/        原始错误代码快照
    repair_attempts/01/   第一次提交；后续为 02、03
    workspace/            工作区，保留最后一次提交
  runs/group_b/           B组任务，每条记录仍有独立的日期编号目录
  runs/group_c/           C组任务，每条记录仍有独立的日期编号目录
```

日期按北京时间，`20261031_001` 表示当天第 1 次实验，下次为 `_002`；逐题目录最后一段是该实验内的执行序号，A/B/C 组编号不重复。三组记录分别放在 runs/group_a/、runs/group_b/、runs/group_c/，每道题仍有独立编号目录。中断后重做尚未保存结果的任务时，会分配新序号，保留原目录的证据。单题 `run` 保存于 `results/runs/group_a（或 group_b、group_c）/日期_序号/`。可用 `--data-dir` 或 Make 的 `DATA_DIR` 指定其他根目录。旧的平铺 runs 布局仍可读取，历史 `var/` 记录保留原位置。

`make experiment` 先显示格式、类型、单元测试、Docker 集成测试和 doctor 检查。正式运行开始时打印实验目录；每个任务结束只打印 A/B/C 组名（group）、重复轮次、策略、题目编号与 passed/failed/error。相邻同题不同策略间留一空行，不同题间留两空行；组别切换时增加两行分割线。执行顺序仍由原有随机调度决定，不为终端排版改变实验顺序。

整批正常结束后，在 Report 路径之前按 A/B/C 顺序统一输出每组最多两个代码案例，按 results.jsonl 的实际记录顺序选取第一个符合条件的任务：A 组一次失败、一次成功各一个；B/C 组首次未成功且实际追加修复后，最终成功、最终仍失败各一个。基础设施异常不当作修复失败案例，B/C 首次成功或只有一次提交的任务不入选。没有符合条件的类别明确说明未出现，不补造案例。继续执行的汇总使用该批次全部已有记录；中断时保存报告，尚不输出最终案例。

案例中显示首次与最终公开/隐藏状态、提交数和原始/最终代码修改行。`- L行号` 是原始代码中被替换或删除的行，`+ L行号` 是最终代码中新增或替换后的行；行号分别对应各自的 solution.py。单题 `run` 保留任务结束即显示修改行的行为。最后打印 report.json 和 report.md 路径。

passed 表示最终公开和隐藏测试均通过，终端标记“修复成功”；failed 表示有效修复仍未通过，修改后的代码标记为“最终候选，尚未修复成功”；error 表示执行异常，不把不完整的结果标记为成功。输出的是实际修改行，不能将所有修改行都认定为已定位的错误行。每轮详细测试诊断和完整统计表仍从日志与报告查看。

金额仅在提供实际日期/模型的价格配置且用量完整时计算；否则为 null，不填零。保留调用次数、输入/输出 token、缓存用量、模型延迟和整题耗时。原始异常请求也计入成本统计。

```bash
make experiment PRICING_FILE=pricing.json
.venv/bin/repair-agent report path/to/report.json
.venv/bin/repair-agent events 20261031_001_001 --data-dir results/experiments/20261031_001
```

报告不再生成 HTML、十张图、统计重采样或自动案例分析报告；终端仅按上述固定规则挑选最多六个案例。人工从原始记录中挑选 3～4 个案例分析；必须包含公开通过但隐藏失败的演示，不编造未出现的现象。

## 简单继续执行

```bash
make experiment RESUME=results/experiments/20261031_001
```

仅读取 config.json 和 results.jsonl，检查基本配置，跳过所有已保存任务，包括正常修复失败与基础设施失败；只执行尚无结果的任务。没有锁、哈希审计或自动失败重试系统。同一批次不要并发启动；代码、题库、镜像或测试变动后另开实验。基础设施失败需人工核对后单独补测，不删除失败证据。

更详细的操作见 [操作手册](docs/OPERATIONS.md)、[实验协议](docs/EXPERIMENT_PROTOCOL.md)。历史接入结果见 [最小测试记录](docs/MINIMAL_API_CHECK.md)。
