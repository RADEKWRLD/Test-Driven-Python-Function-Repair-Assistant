# 测试驱动的 Python 函数修复助手

用于课题 07：研究公开 pytest 失败反馈是否帮助模型真正修复短小纯函数。系统由任务、模型调用、Docker 执行、三组控制、独立隐藏评分、日志与报告六部分组成。

## 固定范围

- 正式题库为完整的 **164 道 FeedbackEval-HumanEval 错误候选**。公开反馈使用冻结的 HumanEval 基础测试，最终隐藏判定使用 HumanEval+ v0.1.10 扩展测试；不复制正确答案或预生成专家反馈。
- 题目一题未删。HumanEval/32 中 7 个连官方参考实现也无法在固定 Docker/Python 3.12 oracle 下稳定通过的数值输入被剔除，规则和数量冻结在 manifest；其余 HumanEval+ 输入全部保留。公开预检为 164/164 初始失败，隐藏参考预检为 164/164 通过。
- 保留 3 道演示题、共 30 个测试函数，覆盖空输入、重复元素、边界和索引问题。
- 正式实验只保留 **DeepSeek API 适配器**，三组固定使用同一模型与参数。
- A 组生成唯一首轮提交；仅当它公开测试失败时，B/C 才从这份完全相同的代码快照分叉，并各自最多追加两次。每个策略的总提交上限仍为 **1/3/3**，完整题库每轮保存 492 条策略结果，物理调用上限 820 次。

| 策略 | 总提交上限 | 模型是否看到详细失败诊断 |
| --- | ---: | --- |
| single-shot | 1 | 生成共享首轮，无后续修复 |
| retry-without-feedback | 3 | 继承共享首轮；失败后只要求重新生成 |
| test-feedback | 3 | 继承共享首轮；提供同一失败补丁的 pytest 输出 |

模型只能通过 `submit_solution(content)` 提交完整 solution.py，没有 shell 或其他文件工具。B/C 公开通过即停止。隐藏结果不反馈给模型。共享首轮消除了三组第一次 API 调用不同造成的随机差异；主比较是在同一个首轮失败样本上计算 C−B 条件修复提升。

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

如果 Docker Desktop 显示代理为 `http.docker.internal:3128`，但构建容器仍无法连接 Debian 软件源，可显式执行：

```bash
docker build \
  --build-arg HTTP_PROXY=http://http.docker.internal:3128 \
  --build-arg HTTPS_PROXY=http://http.docker.internal:3128 \
  -f docker/sandbox-python.Dockerfile \
  -t function-repair/sandbox-python:dev .
```

Docker Desktop/Engine 在测试和实验期间保持运行。主控制器调用模型 API，候选代码只在断网、资源受限、根文件系统及 workspace 只读的 Docker 中执行。密钥、个人目录和原始题库不会挂载给候选代码；隐藏测试只在修复结束后的评测容器挂载。

已有 `.env` 时保留它；首次配置可复制 `.env.example`，自行填写密钥，不在聊天或日志中公开。

```text
DEEPSEEK_API_KEY=在本地填写
REPAIR_ASSISTANT_MODEL=deepseek-flash
```

## 从演示到正式实验

```bash
# 三道演示题，三组一轮，共 9 个 run
make experiment TASKS_DIR=benchmarks/tasks

# 默认：完整 164 道 FeedbackEval-HumanEval，保存 492 条策略结果
make experiment

# 单题调试
.venv/bin/repair-agent run benchmarks/tasks/chunk-list --strategy test-feedback
```

测试和正式实验会调用已配置的模型并产生实际费用。重复实验是可选扩展，需显式设置 `REPETITIONS=3`；默认一轮即可，不自动增加预算。

## 日志、评分与简洁报告

每轮保存代码、模型请求/响应和公开反馈，使用普通 JSONL 日志。公开测试仍有只读保护与文件校验；去掉日志哈希链不影响测试保护。

修复完全停止后，独立评分首次/最终公开和 HumanEval+ 隐藏测试；原始错误函数只做一次轻量隐藏评分，用于检查原本正确的测试函数是否被改坏。回归按现有 pytest 测试函数的 passed→failed 统计。164 道题、候选覆盖、来源哈希、oracle 筛选及两份预检结果均冻结在题库目录中。精确期望输出只保存稳定摘要，需要浮点容差的输出才保存数值；模型无法挂载隐藏目录。

```text
results/experiments/20261031_001/
  config.json             基本实验配置
  results.jsonl           每个 run 结束后立即保存的结果
  report.json             机器可读汇总
  raw-runs.csv            原始逐 run 数据
  feedbackeval-repair-histories.jsonl  FeedbackEval 风格逐轮代码与反馈轨迹
  strategy-metrics.csv    三组汇总
  test-results.csv        隐藏测试函数的结果变化
  report.md               唯一的课程报告，含人工错误分析区
  figures/*.svg           六张图，另含共享首轮失败后的条件修复率
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

`make experiment` 先运行格式、类型、单元测试、Docker 集成测试和 doctor。题目×重复单元按种子随机化；每个单元必须先执行共享 A，B/C 的分支先后再由原调度随机决定。终端随后打印策略、题目与结果。

整批正常结束后，在 Report 路径之前按 A/B/C 顺序统一输出每组最多两个代码案例，按 results.jsonl 的实际记录顺序选取第一个符合条件的任务：A 组一次失败、一次成功各一个；B/C 组首次未成功且实际追加修复后，最终成功、最终仍失败各一个。基础设施异常不当作修复失败案例，B/C 首次成功或只有一次提交的任务不入选。没有符合条件的类别明确说明未出现，不补造案例。继续执行的汇总使用该批次全部已有记录；中断时保存报告，尚不输出最终案例。

案例中显示首次与最终公开/隐藏状态、提交数和原始/最终代码修改行。`- L行号` 是原始代码中被替换或删除的行，`+ L行号` 是最终代码中新增或替换后的行；行号分别对应各自的 solution.py。单题 `run` 保留任务结束即显示修改行的行为。最后打印 report.json 和 report.md 路径。

passed 表示最终公开和隐藏测试均通过，终端标记“修复成功”；failed 表示有效修复仍未通过，修改后的代码标记为“最终候选，尚未修复成功”；error 表示执行异常，不把不完整的结果标记为成功。输出的是实际修改行，不能将所有修改行都认定为已定位的错误行。每轮详细测试诊断和完整统计表仍从日志与报告查看。

金额仅在提供实际日期/模型的价格配置且用量完整时计算；否则为 null，不填零。策略表将共享首轮归因给 B/C，以表示策略独立运行的等价成本；报告另列物理实际成本，只计算一次共享首轮和两个分支真实新增的调用。

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
