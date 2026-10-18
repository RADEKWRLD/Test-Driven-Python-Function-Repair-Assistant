# Test-Driven Python Function Repair Assistant

一个用于研究“pytest 失败反馈是否真正帮助模型修复 Python 函数”的小型可复现课设。

完整的本机验收、对照实验、指标口径和答辩流程见
[`docs/OPERATIONS.md`](docs/OPERATIONS.md)。

项目只处理短小纯函数，比较三种策略：

- `single-shot`：只允许一次修复；
- `retry-without-feedback`：最多五次，控制器运行公开 pytest；失败时只要求重新生成，不提供诊断；
- `test-feedback`：最多五次，使用相同的 pytest 与停止规则，并把完整失败输出交给下一轮。

模型没有 shell，也不能执行任何代码；每轮只有一次模型调用，并且只能通过
`submit_solution(content)` 提交完整的 `solution.py`。两个多次提交组都由控制器执行
公开测试并在通过时停止，唯一差异是模型能否看到详细诊断；三组结束后再由统一的
隔离评测器对首轮和最终快照评分。
所有候选代码只在无网络、受资源限制的 Docker 容器中执行。API Key、个人文件、
原始基准目录和隐藏测试不会进入容器。

## 快速开始

```bash
python3.12 -m venv .venv
.venv/bin/pip install -e '.[dev]'
make sandbox-build
.venv/bin/repair-agent doctor
```

从项目根目录的 `.env` 注入 DeepSeek API Key（只供宿主控制面调用模型，不会传入 Docker 容器）：

```bash
cp .env.example .env
# 编辑 .env，填写 DEEPSEEK_API_KEY
chmod 600 .env
.venv/bin/repair-agent run benchmarks/tasks/public-pass-hidden-fail \
  --strategy test-feedback
```

运行全部三组对照实验：

```bash
make experiment
```

该命令会先完成本地及 Docker 验收，再以最多 5 次提交、固定 seed 和 1 次重复运行实验。可按需覆盖参数，例如：

```bash
make experiment REPETITIONS=1 SEED=42 MODEL=deepseek-chat
```

聚合报告会分策略输出首次/最终公开与隐藏测试通过率、超时率、隐藏功能回归率、保护测试违规率和真实模型调用/token/延迟。实验结束后会自动生成 10 张 SVG 图、HTML 总览、Markdown 报告以及逐 run 和逐策略 CSV。由于模型价格会变，程序保留原始 token 用量，`currency_cost` 不做猜测而记为 `null`。

实验报告目录如下：

```text
var/benchmarks/benchmark-<UTC时间>/
├── report.json
├── report.html
├── report.md
├── raw-runs.csv
├── strategy-metrics.csv
├── manifest.json
└── figures/*.svg
```

已有 benchmark JSON 也可以重新生成图表：

```bash
.venv/bin/repair-agent report path/to/benchmark.json
```

一次 run 的产物位于 `var/runs/<run_id>/`：

```text
events.jsonl             # 只追加、带哈希链的过程日志
summary.json             # 首次/最终隐藏测试、超时和成本
workspace/               # 控制器维护的最终候选工作区
attempts/attempt-*/       # 每轮提交时的代码快照
```

## 基准与隐藏测试

`benchmarks/tasks/` 中提供 3 道纯函数题，共 30 个 pytest 测试函数，覆盖空输入、重复元素、边界值和索引错误。

```text
task.json                 # 需求、公开验证命令、隐藏验证命令
workspace/                # 错误函数与公开测试；只把文本放入模型上下文
hidden_tests/             # 不复制、不挂载给 Agent
```

隐藏测试只在修复过程停止后由独立 verifier 容器以只读方式挂载；结果不会回馈给模型。`public-pass-hidden-fail` 的初始实现会通过公开测试但在制表符、换行和连续空格等隐藏边界上失败，用于现场演示“公开通过 ≠ 真正修复”。

### HumanEvalPack 50 题

`benchmarks/humanevalpack/` 已冻结 50 道 Python 修复题。筛选器先排除空测试和语法损坏记录，再在受限 Docker 中确认错误实现会使公开 pytest 正常失败；同时要求至少 2 个公开断言、至少 5 个隐藏断言且隐藏测试更多。最后按 bug 类型分层，并优先保留控制流和隐藏断言更复杂的题。标准答案不会写入仓库。

重新下载和生成一批任务时使用：

```bash
make dataset-bootstrap
# 公开数据集通常不要求登录；需要令牌时只设置环境变量 HF_TOKEN
.venv/bin/repair-agent import-humanevalpack benchmarks/humanevalpack-new \
  --limit 50 --seed 20261018 --selection useful
```

对冻结的 50 题运行三组实验：

```bash
make experiment TASKS_DIR=benchmarks/humanevalpack REPETITIONS=1
```

这会产生 `50 × 3 × 1 = 150` 个 run。正式重复 3 次则是 450 个 run：

```bash
make experiment TASKS_DIR=benchmarks/humanevalpack REPETITIONS=3
```

## 验收

```bash
make check               # 格式、静态类型和单元测试
make sandbox-test        # 需要本机 Docker daemon 和已构建镜像
```

实验数据不预填模拟结果；未实际运行的指标为 `null` 或不存在。
