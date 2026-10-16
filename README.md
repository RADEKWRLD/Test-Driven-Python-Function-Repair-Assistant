# Test-Driven Python Function Repair Assistant

一个用于研究“pytest 失败反馈是否真正帮助模型修复 Python 函数”的小型可复现课设。

项目只处理短小纯函数，比较三种策略：

- `single-shot`：只允许一次修复；
- `retry-without-feedback`：最多三次，但不把控制器的 pytest 结果交给下一轮；
- `test-feedback`：最多三次，把确定性 pytest 输出加入下一轮记忆。

Agent 只拥有一个容器内 `shell` tool。容器默认断网、限制 CPU/内存/进程数、丢弃 Linux capabilities，且只挂载本次 run 的 workspace。API Key、个人文件、原始基准目录和隐藏测试都不会进入 Agent 容器。

## 快速开始

```bash
python3.12 -m venv .venv
.venv/bin/pip install -e '.[dev]'
make sandbox-build
.venv/bin/repair-agent doctor
```

设置 DeepSeek API Key（只供宿主控制面调用模型）：

```bash
export DEEPSEEK_API_KEY=...
.venv/bin/repair-agent run benchmarks/tasks/public-pass-hidden-fail \
  --strategy test-feedback
```

运行全部三组对照实验：

```bash
.venv/bin/repair-agent benchmark benchmarks/tasks
```

聚合报告会分策略输出首次/最终公开与隐藏测试通过率、超时率、隐藏功能回归率、保护测试违规率和真实模型调用/token/延迟。由于模型价格会变，程序保留原始 token 用量，`currency_cost` 不做猜测而记为 `null`。

一次 run 的产物位于 `var/runs/<run_id>/`：

```text
events.jsonl             # 只追加、带哈希链的过程日志
summary.json             # 首次/最终隐藏测试、超时和成本
workspace/               # 最终 Agent 工作区
attempts/attempt-*/       # 每轮提交时的代码快照
```

## 基准与隐藏测试

`benchmarks/tasks/` 中提供 3 道纯函数题，共 30 个 pytest 测试函数，覆盖空输入、重复元素、边界值和索引错误。

```text
task.json                 # 需求、公开验证命令、隐藏验证命令
workspace/                # 复制给 Agent，包含错误函数和公开测试
hidden_tests/             # 不复制、不挂载给 Agent
```

隐藏测试只在 Agent 停止后由独立 verifier 容器以只读方式挂载；结果不会回馈给模型。`public-pass-hidden-fail` 的初始实现会通过公开测试但在制表符、换行和连续空格等隐藏边界上失败，用于现场演示“公开通过 ≠ 真正修复”。

## 验收

```bash
make check               # 格式、静态类型和单元测试
make sandbox-test        # 需要本机 Docker daemon 和已构建镜像
```

实验数据不预填模拟结果；未实际运行的指标为 `null` 或不存在。
