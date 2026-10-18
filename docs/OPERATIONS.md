# 操作手册与验收口径

本文档用于完成课题 07 的本机验收、真实对照实验、结果解读和答辩演示。

## 1. 当前完成状态

### 已实现

- 三种策略：`single-shot`、`retry-without-feedback`、`test-feedback`。
- 默认一次初始提交；两个多次提交组最多再提交四次，并在公开测试通过时停止，即硬上限 5 次。
- 每次提交只有一次模型调用；模型没有 shell，只能通过 `submit_solution(content)` 提交完整 `solution.py`。
- `single-shot` 修复阶段不运行 pytest；两个多次提交组每次提交后都运行相同的公开 pytest，并在通过时停止。无反馈组失败后只收到重新生成要求，反馈组收到完整失败诊断。
- 公开测试在修复开始前计算 SHA-256 基线，修改、增加或删除受保护测试都会使验证失败。
- 每个任务显式声明 `editable_paths`；当前三题均只允许修改 `solution.py`。pytest 前后都会检查完整 workspace，新增、删除或修改其他路径都会使该轮失败。
- 隐藏测试不进入模型上下文，只在修复停止后挂载给独立 verifier，并且隐藏结果不反馈给模型。
- 隐藏验证时，attempt workspace 与隐藏测试都使用只读挂载。
- Docker 执行器使用无网络、只读根文件系统、能力丢弃、`no-new-privileges`、CPU、内存、PID、超时和有限 `/tmp`。
- 每轮保存代码快照、模型请求与响应、solution 提交、可用的 pytest 输出、token、延迟和带哈希链的事件日志。
- 3 个任务共 30 个独立测试函数：15 个公开测试、15 个隐藏测试。
- 已冻结 50 道经过静态检查、公开失败预检、复杂度排序和 bug 类型分层的 HumanEvalPack Python 任务；标准答案未保存。
- 聚合报告包含首次/最终公开与隐藏通过率、超时、隐藏回归、测试保护违规、模型调用数、token 和模型延迟。
- benchmark 支持重复次数、固定 seed 的随机执行顺序，以及同一报告内的跨重复聚合。
- 最大提交次数在 CLI 和控制器两层硬限制为 5。
- `public-pass-hidden-fail` 可演示“5 个公开测试通过，但 5 个隐藏测试全部失败”。

### 尚未完成或需要加强

1. `var/benchmarks/benchmark-20261018T001614215512Z/` 使用旧的“无反馈组固定重试”协议，不能作为新协议的正式结果；修改后需要重新运行 benchmark。
2. `currency_cost` 当前为 `null`。程序记录了实际调用数和 token，但若验收要求人民币或美元成本，需要锁定实验日期对应的模型价格并离线计算。
3. 3 道题只能用于课程演示，不足以支持强统计结论；即使增加重复次数，也最好继续增加题目数和错误类型。
4. `retry-without-feedback` 会从“继续重试”获得隐含的二值失败信号，但看不到失败用例、异常、stdout/stderr；报告中应将它准确解释为“无诊断反馈”，而不是完全没有任何信号。
5. 当前超时率包含修复期和最终评测的公开/隐藏验证超时；模型不能执行 shell。成本只统计模型 API 延迟，不等同于端到端运行时间。
6. 错误分析所需原始轨迹已经具备，但仓库还没有基于真实 run 编写的错误分类与案例分析报告。

## 2. 一次性安装

要求：Python 3.12+、Docker Desktop、可用的 DeepSeek API Key。

```bash
python3.12 -m venv .venv
.venv/bin/pip install -e '.[dev]'
make sandbox-build
```

如果 Docker Desktop 已配置代理，但构建时 APT 仍然超时，显式传入构建代理：

```bash
docker build \
  --build-arg HTTP_PROXY=http://http.docker.internal:3128 \
  --build-arg HTTPS_PROXY=http://http.docker.internal:3128 \
  -f docker/sandbox-python.Dockerfile \
  -t function-repair/sandbox-python:dev .
```

不要使用 `export`，也不要把 API Key 写入 Dockerfile、镜像、任务 workspace 或提交到 Git。复制项目提供的模板，创建被 `.gitignore` 排除的 `.env`：

```bash
cp .env.example .env
```

然后只在本机编辑 `.env`：

```text
DEEPSEEK_API_KEY=你的密钥
REPAIR_ASSISTANT_MODEL=deepseek-chat
```

建议限制文件权限：

```bash
chmod 600 .env
```

## 3. 每次实验前的硬性检查

```bash
.venv/bin/repair-agent doctor
make check
make sandbox-test
```

合格结果应同时满足：

- `doctor` 输出 `Sandbox image: ready`；
- Ruff 与 mypy 无错误；
- 20 个非 Docker 测试通过；
- 1 个 Docker 集成测试通过。

任何一项失败都不要运行真实模型实验。尤其不要为了绕过 Docker 问题而直接在宿主 Python 中执行候选代码。

为了保证结果可复现，实验前还应记录：

```bash
git rev-parse HEAD
docker image inspect function-repair/sandbox-python:dev \
  --format '{{json .RepoDigests}} {{.Id}}'
python3 --version
docker version --format '{{.Server.Version}}'
```

若镜像没有远端 digest，至少记录镜像 ID。

## 4. 单题冒烟实验

先分别跑同一题的三种策略，确认 API、日志和隐藏验证链路都正常：

```bash
.venv/bin/repair-agent run benchmarks/tasks/chunk-list \
  --strategy single-shot --max-attempts 5

.venv/bin/repair-agent run benchmarks/tasks/chunk-list \
  --strategy retry-without-feedback --max-attempts 5

.venv/bin/repair-agent run benchmarks/tasks/chunk-list \
  --strategy test-feedback --max-attempts 5
```

`single-shot` 内部会强制只提交一次；统一写 `--max-attempts 5` 便于保留一致的实验命令。

每次运行会输出 `run_id` 和 `summary.json` 路径。检查摘要：

```bash
python -m json.tool var/runs/<run_id>/summary.json
.venv/bin/repair-agent events <run_id>
```

一次 run 的关键证据位于：

```text
var/runs/<run_id>/events.jsonl
var/runs/<run_id>/summary.json
var/runs/<run_id>/workspace/
var/runs/<run_id>/attempts/attempt-1/
var/runs/<run_id>/attempts/attempt-2/
var/runs/<run_id>/attempts/attempt-3/
var/runs/<run_id>/attempts/attempt-4/
var/runs/<run_id>/attempts/attempt-5/
```

`events` 命令显示 `Integrity: OK` 才能把该日志纳入结果。

## 5. 标准对照实验

推荐使用自定义 Make 启动命令，它会先执行 `make check`、Docker 集成测试和 `doctor`，全部通过后才开始真实模型实验：

```bash
make experiment
```

默认参数等价于：

```bash
.venv/bin/repair-agent benchmark benchmarks/tasks \
  --max-attempts 5 \
  --repetitions 1 \
  --seed 20261016 \
  --model deepseek-chat
```

需要低成本冒烟或更换实验配置时，可覆盖 Make 变量：

```bash
make experiment REPETITIONS=1 SEED=42 MODEL=deepseek-chat
```

上述默认命令执行 3 道题 × 3 种策略 × 1 次重复，共 9 个 run，并生成：

```text
var/benchmarks/benchmark-<UTC时间>/
├── report.json                 # 聚合指标与全部 raw_runs
├── report.html                 # 可直接打开的可视化总览
├── report.md                   # 适合纳入课题报告的图文索引
├── raw-runs.csv                # 逐 run 可复核明细
├── strategy-metrics.csv        # 逐策略聚合指标
├── manifest.json               # 产物清单
└── figures/                    # 10 张无外部依赖的 SVG 图
```

正式比较时固定以下控制变量，不要在组间改变：

- Git commit 与 Docker 镜像 ID；
- 模型名称、API 提供方、temperature 和最大输出 token；
- 任务集合、重复次数与随机化 seed；
- `max-attempts=5`，且每次提交固定一次模型调用；
- 容器 CPU、内存、PID 和测试超时；
- 同一时间段或随机化后的运行顺序，避免服务端模型更新和负载变化造成偏差。

`--repetitions` 会重复每个“题目 × 策略”组合；所有 job 由 `--seed` 确定性打乱，实际执行顺序写入报告的 `design.execution_order`。同一个 benchmark 命令产生的所有重复会在同一份报告中按策略聚合。默认 1 次是为了防止开发阶段意外产生大量 API 调用；正式实验建议显式指定 3～5 次。再次运行时保留相同 seed 可复现实验顺序，换 seed 可进行另一批随机化重复。

### 5.1 HumanEvalPack 50 题实验

仓库中的 `benchmarks/humanevalpack/` 来自固定 revision 的 Python split。164 条源记录中有 157 条通过静态检查；进一步要求至少 2 个公开断言、至少 5 个隐藏断言且隐藏断言更多，得到 111 条；其中 96 条错误实现会在受限 Docker 中让公开 pytest 正常失败。最终按 bug 类型分层，并优先选取控制流与测试覆盖更复杂的 50 条。筛选清单位于 `dataset-manifest.json`，仓库不保存 `canonical_solution`。

重新生成到一个不存在的新目录（导入器拒绝覆盖已有目录）：

```bash
make dataset-bootstrap
.venv/bin/repair-agent import-humanevalpack benchmarks/humanevalpack-new \
  --limit 50 \
  --seed 20261018 \
  --selection useful
```

HumanEvalPack 是公开数据集，正常情况下不需要登录。若 Hugging Face 对当前网络要求认证或提高限流，可在宿主环境设置 `HF_TOKEN`；该令牌不会进入生成任务或 Docker 容器。

先做单次重复的完整三组实验：

```bash
make experiment TASKS_DIR=benchmarks/humanevalpack REPETITIONS=1
```

运行数由下式决定：

```text
任务数 × 策略数 × 重复数
50 × 3 × 1 = 150 run
50 × 3 × 3 = 450 run
```

每个 run 内，`single-shot` 固定调用模型 1 次；另外两组公开测试通过即停止，最多调用 5 次。因此 150 个 run 不等于固定 750 次模型调用。

## 6. 指标体系

### 6.1 主指标

主指标只使用：**最终隐藏测试通过率**。

```text
FinalHiddenPassRate(strategy)
  = 最终隐藏测试通过的 run 数 / 该策略总 run 数
```

回答“测试反馈是否有帮助”的核心效应量是：

```text
FeedbackEffect
  = FinalHiddenPassRate(test-feedback)
  - FinalHiddenPassRate(retry-without-feedback)
```

`retry-without-feedback` 与 `test-feedback` 的最大提交次数相同，所以二者差值比单独比较 `single-shot` 更能回答研究问题。`single-shot` 用于说明追加机会本身带来的收益。

### 6.2 必须同时报告的次指标

| 指标 | 计算方式 | 用途 |
| --- | --- | --- |
| 首次隐藏通过率 | 首轮隐藏通过 run / 总 run | 三组初始能力是否相近 |
| 最终公开通过率 | 最终公开通过 run / 总 run | 只看公开测试时的表面成功 |
| 公隐差距 | 最终公开通过率 - 最终隐藏通过率 | 过拟合公开测试的程度 |
| 隐藏提升率 | 首轮隐藏失败且最终隐藏通过 / 总 run | 后续修正真正救回了多少任务 |
| 隐藏回归率 | 首轮隐藏通过但最终隐藏失败 / 总 run | 后续修正是否破坏已有功能 |
| 超时率 | 出现控制器验证超时的 run / 总 run | 可靠性与拒绝服务风险 |
| 测试保护违规率 | 修改受保护测试的 run / 总 run | 安全约束遵守情况 |
| workspace 策略违规率 | 修改 `solution.py` 之外路径的 run / 总 run | 文件白名单执行情况 |
| 平均模型调用数 | 模型调用总数 / run 数 | API 调用负担 |
| 平均 token | total token / run 数 | 主要成本代理指标 |
| 每成功成本 | total token / `outcome=passed` 的 run 数 | 成本效益；报告字段为 `tokens_per_success` |
| 模型延迟 | API 延迟总和或每 run 均值 | 性能参考，不等于端到端时间 |

不要把“最终公开通过率”作为主指标；它正是容易产生“看似修好”结论的指标。

### 6.3 货币成本

实验结束后保存模型供应商当日价格版本，并按 prompt 与 completion 分开计算：

```text
currency_cost
  = prompt_tokens × prompt_unit_price
  + completion_tokens × completion_unit_price
```

如果无法锁定价格，保留 `currency_cost=null`，报告原始 token；不要使用不明日期的价格补算。

### 6.4 统计表达

- 3 道题各跑一次时只能报告描述性结果，例如 `2/3`，不应声称具有统计显著性。
- 有重复实验时，同时报告分子/分母、百分比和 95% 置信区间。
- 同一个任务和重复编号下的两种策略应视为配对观察；报告配对差值时按任务聚类 bootstrap，避免把同一道题的重复运行误当成独立任务。样本足够时可另做 McNemar 检验。
- 如果只保留 3 道题，应将结论限定为“在本课程 benchmark 上”；要推广到一般 Python 函数修复，应增加任务数量和错误类型。

## 7. 自动可视化报告

`benchmark` 完成后会自动生成以下图表：

1. 测试反馈相对无反馈重试的配对主效应、按任务聚类的 bootstrap 95% CI，以及胜/平/负数量；
2. 三种策略的首次与最终隐藏通过率，并显示 Wilson 95% CI；
3. 最终公开与最终隐藏通过率及公隐差距；
4. 隐藏结果从首次到最终的改善、稳定通过、回归和稳定失败；
5. 超时、测试保护违规和 workspace 策略违规率；
6. 平均模型调用、平均 token、每成功 token 和平均模型延迟；
7. prompt/completion token 构成；
8. “策略 × 任务”的最终隐藏通过率热力图；
9. 各重复编号的最终隐藏通过率趋势；
10. 各策略实际提交次数分布。

重新绘制已有聚合 JSON：

```bash
.venv/bin/repair-agent report path/to/benchmark.json
```

指定输出目录：

```bash
.venv/bin/repair-agent report path/to/benchmark.json \
  --output-dir var/benchmarks/rebuilt-report
```

答辩时优先打开 `report.html`。论文或课程报告可直接引用 `figures/*.svg`；需要进一步使用 R、Excel 或 Python 分析时，使用两份 CSV，而不要从 SVG 反推数据。

## 8. 如何判定课题完成

### 工程验收门槛

- `make check` 与 `make sandbox-test` 全部通过；
- `doctor` 通过；
- 生成代码从未在宿主执行；
- 模型看不到隐藏测试，隐藏结果不进入后续模型上下文；
- 模型没有 shell，且只能提交 `solution.py`；
- 两个多次提交组使用相同的公开 pytest 和通过即停止规则，只有详细诊断是否回传不同；
- 每轮快照与完整事件日志存在且哈希链可验证；
- 文件白名单生效，除允许的实现文件外不能修改或新增文件；
- 后两组的提交上限相同，`single-shot` 固定一次；
- 30 个测试函数被自动检查。

### 实验验收门槛

- 至少完成一轮 9-run 对照实验；
- 报告三组的主指标、次指标和实际 token/调用成本；
- 明确比较 `test-feedback` 与 `retry-without-feedback`；
- 对公开通过但隐藏失败、超时、回归和测试违规逐类分析；
- 保留原始 `summary.json`、`events.jsonl`、attempt 快照和聚合报告；
- 不把小样本描述性差异写成普遍因果结论。

只有工程门槛和实验门槛都满足，才能说课题成果完整。当前仓库已达到工程原型要求，但仍需运行真实实验、补充更多题目、按实验日期计算货币成本并完成错误分析报告。

## 9. 答辩演示流程

1. 运行 `.venv/bin/repair-agent doctor`，展示隔离环境可用。
2. 打开 `docker/sandbox-python.Dockerfile` 和 `src/repair_assistant/sandbox.py`，说明无网络、资源限制和挂载边界。
3. 展示 `benchmarks/tasks/public-pass-hidden-fail`：公开测试 5/5 通过，隐藏测试 0/5 通过。
4. 运行一个 `test-feedback` 任务，展示失败输出如何进入下一轮。
5. 用 `repair-agent events <run_id>` 验证日志哈希链，再展示 `attempt-1` 与最终 attempt 的代码差异。
6. 打开 benchmark JSON，只先讲最终隐藏通过率，再讲公隐差距、回归率和成本。
7. 最后主动说明样本量、模型随机性、无反馈组仍有隐含二值失败信号，以及文件白名单等效度威胁。

## 10. 常见故障

### APT 显示 `Unable to locate package`

先看前面的 `apt-get update` 是否网络超时。索引未下载时，包不存在只是后续症状。Docker Desktop 代理环境可使用第 2 节的显式 `--build-arg` 命令。

### `Sandbox image: not built`

运行 `make sandbox-build`，代理环境使用第 2 节的替代命令，然后重新运行 `doctor`。

### 实验中断

不要手工修改已生成的 run 目录。保留失败 run 作为异常证据，重新启动一个新 run；run ID 是唯一的。

### API Key 缺失

CLI 会在发起实验前退出。检查 `.env` 或当前 shell 的 `DEEPSEEK_API_KEY`，不要把 Key 传给容器或写入命令日志。

### `CERTIFICATE_VERIFY_FAILED`

项目默认使用 `certifi` 的 Mozilla CA 根证书，不依赖 Python Framework 是否安装了系统 `cert.pem`。修改依赖后先执行：

```bash
.venv/bin/pip install -e '.[dev]'
```

如果所在组织使用私有 HTTPS 根证书，将 PEM 证书包路径写入 `.env`，不要关闭 SSL 验证：

```dotenv
REPAIR_ASSISTANT_CA_BUNDLE=/absolute/path/to/organization-ca-bundle.pem
```
