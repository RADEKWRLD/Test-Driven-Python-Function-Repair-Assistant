# 操作手册（精简版）

当前范围和指标以 [实验协议](EXPERIMENT_PROTOCOL.md) 为准；正式题库为完整164道 FeedbackEval-HumanEval，采用共享首轮分叉和三组1/3/3预算。

## 本机启动

1. 打开 Docker Desktop，等待引擎运行，整个测试/实验期间保持开启。
2. 打开 Ubuntu-22.04 终端。
3. 进入项目，使用已有 Linux 虚拟环境：

```bash
cd /mnt/e/Python函数修复助手/Test-Driven-Python-Function-Repair-Assistant
.venv/bin/python --version
.venv/bin/repair-agent doctor
make check
make sandbox-test
```

已有 `.venv` 无需重建，也无需激活。系统 Python/mambaunet 仍是 3.10，项目使用独立 3.12。全新环境安装步骤见 README。沙箱镜像已构建；镜像不存在或 Dockerfile 变化时执行 `make sandbox-build`。

doctor 只检查 Python、Docker CLI/引擎和镜像，不能代替 Docker 集成测试。任何环境验收失败，都先修复环境，不在宿主执行候选代码。

## 模型配置

已有 `.env` 中的密钥不覆盖、不输出。默认使用实际接入过的 DeepSeek 配置：

```text
DEEPSEEK_API_KEY=在本地填写
REPAIR_ASSISTANT_MODEL=deepseek-flash
```

三组必须共用同一个模型配置，不能中途切换提供方。DeepSeek 密钥只用于宿主 API 请求，不传入 Docker 容器。

## 演示与正式实验

下列命令会调用模型并可能产生实际费用；本次代码精简不自动执行它们。

```bash
# 单题调试
.venv/bin/repair-agent run benchmarks/tasks/chunk-list --strategy test-feedback

# 三道演示题，9 个 run
make experiment TASKS_DIR=benchmarks/tasks

# 164 道正式题，保存492条策略结果；最坏820次物理调用
make experiment
```

每道题先由A生成一次共享首轮；公开失败后B/C继承同一快照并各自最多追加两次，公开通过即停止。重复实验需显式设置 `REPETITIONS=3`。

现有164题已经冻结，正式运行无需联网下载数据。可复现导入脚本保留在 `tools/import_feedbackeval_humaneval_full.py`，不会在实验时执行。题库目录中的 `preflight.json` 应为 164 个初始公开失败、0 超时；`hidden-reference-preflight.json` 应为 164 个参考隐藏通过、0 超时。manifest 记录 HumanEval+ v0.1.10 来源哈希及 7 个 oracle 无效/跨版本不稳定输入的剔除数量。

## 结果与人工分析

默认根目录为 results。正式实验保存于 results/experiments/日期_序号/，例如 20261031_001；日期按北京时间，同一天的新实验递增编号。逐题记录按组分开保存于 runs/group_a/、runs/group_b/、runs/group_c/，其下每个日期_实验序号_执行序号目录保存一个任务，含 events.jsonl、summary.json、original_code/、repair_attempts/01/（后续 02、03）和 workspace/。三组的执行编号不重复，题目和策略记录于 summary.json。中断后重做尚无批次结果的任务时分配新序号，保留原目录。单题调试使用 results/runs/group_a（或 group_b、group_c）/日期_序号/。events 命令按编号自动查找组目录，并兼容旧的平铺 runs 布局。

events 是普通 JSONL，不做防篡改验证；公开测试文件保护仍保持原来的哈希校验和只读限制。历史 var/ 记录保留原位置。

题目×重复单元按seed随机化。每个单元必须先生成共享A；B/C分支先后按随机调度决定。终端逐条打印组、重复、题目和结果。

整批正常结束后、Report 地址之前，统一按 A/B/C 组输出每组最多两个代码案例，按实际记录顺序选择：A 组第一个一次失败与第一个一次成功；B/C 组第一个首次失败但追加修复后成功，以及第一个首次失败且追加修复后仍失败。首次失败以首次公开或隐藏至少一项未通过判断；最终成功需公开和隐藏均通过。只有一次提交的 B/C 任务、基础设施异常不入选；没有符合条件的类别注明未出现。继续执行时从全批次记录选取，中断不输出最终案例。

案例附首次与最终公开/隐藏状态、提交数和原始/最终代码差异；`- L行号` 对应原始 solution.py 中替换或删除的行，`+ L行号` 对应最终提交中新增或替换后的行。单题 run 仍在任务结束时打印代码修改行。最后打印 Report（JSON）与 Course report（Markdown）路径。

passed 要求最终公开和隐藏均通过，才将最终代码标记为“修复成功”；failed 显示“尚未修复成功”的最终候选代码；error 不冒充成功。终端比较原始与最终代码，不把每个修改行都认定为已定位的错误行；每轮详细诊断和汇总指标从文件查看。没有代码变化或快照缺失时明确提示，不中断实验。

每批实验生成：

当前从 /mnt/e/Python函数修复助手/Test-Driven-Python-Function-Repair-Assistant 运行，结果实际保存在 Windows 的 E:\Python函数修复助手\Test-Driven-Python-Function-Repair-Assistant\results\experiments\日期_序号\。可用 VS Code 左侧文件树打开 report.md，按 Ctrl+Shift+V 预览；WSL 和 Windows 访问的是同一份文件。每次运行终端打印的 Experiment、Report 路径是实际位置。

```text
config.json
results.jsonl
report.json
raw-runs.csv
strategy-metrics.csv
test-results.csv
report.md
figures/hidden-pass-rates.svg
figures/public-hidden-gap.svg
figures/reliability.svg
figures/conditional-repair.svg
figures/cost.svg
```

打开 report.md，先看共享首轮失败数、B/C条件隐藏通过率、C独赢与B独赢，再看总体隐藏通过率、公隐差距、回归、超时和物理实际成本。

```bash
.venv/bin/repair-agent events 20261031_001_001 --data-dir results/experiments/20261031_001
.venv/bin/repair-agent report path/to/report.json
```

旧日志仍可读取，旧报告/历史最小测试产物保留，但不混入新的精简批次。重建旧 JSON 报告也使用当前五图 Markdown 生成器。

## 保存、跳过与异常

每个 run 结束立即保存结果，正常失败属于有效实验数据。基础设施异常保留状态和已有调用成本，跳过后继续运行其他题。

```bash
make experiment RESUME=results/experiments/20261031_001
```

该命令只执行尚未保存在 results.jsonl 中的任务，已保存的成功、正常失败和异常均跳过。保持模型、题库、重复数、seed、价格和数据目录等基本配置相同；配置不符会拒绝执行。取消 `--retry-errors`，基础设施失败由人工查明原因后单题补测并保留原失败记录。

没有复杂锁与哈希审计，不要并发使用同一批次目录，不要手动改 results.jsonl；代码、测试、题库或镜像变化后新建实验。异常强杀造成半行 JSON 时，应先保留原文件、人工检查尾部，再继续执行。

## 实际金额

提供可靠价格配置时：

```bash
make experiment PRICING_FILE=pricing.json
```

单价字段与要求见实验协议。没有价格或用量时金额显示 N/A/null；不是零费用。余额差受精度和入账延迟影响，准确账单以供应商记录为准。API 延迟、测试耗时和整题耗时分别记录，不把 API 延迟当总耗时。

## 答辩最小流程

1. 展示 doctor 和 Docker 隔离设置。
2. 展示一个测试反馈修复 run 的每轮代码与公开诊断。
3. 展示 public-pass-hidden-fail 题：公开通过仍可能隐藏失败。
4. 用三组结果回答反馈是否有收益及成本代价。
5. 展示真实案例、回归和超时记录，并说明样本与模型版本限制。
