# 实验设计与验收方案

## 1. 研究问题

在模型、题目、tool 权限、最大 turn 和最大提交次数可比的前提下，将确定性 pytest 失败输出加入模型记忆，是否会提高最终隐藏测试通过率，而不只是提高公开测试通过率？

## 2. 自变量与对照组

| 策略 | 初始提交 | 追加修复 | 控制器 pytest 失败输出 |
| --- | ---: | ---: | --- |
| `single-shot` | 1 | 0 | 不回馈 |
| `retry-without-feedback` | 1 | 最多 4 | 不回馈，下一次使用新对话记忆 |
| `test-feedback` | 1 | 最多 4 | 回馈 exit code、timeout、stdout、stderr 和测试保护违规 |

两个多次尝试组都是最多 5 次提交、每次最多 12 个模型 turn；提交次数在 CLI 和 Agent 两层硬限制为 5。三组都拥有相同的容器 `shell` tool，因此模型主动运行 pytest 属于 Agent 行为；组间差异只是 Agent 停止一次提交后，控制器是否将独立验证的失败输出写入下一轮记忆。

## 3. 执行协议

1. 控制面复制 `workspace/` 到唯一 run 目录，对公开测试做 SHA-256 基线。
2. Agent 容器只挂载该 run 的 workspace；`hidden_tests/`、`.env`、事件日志和 Docker socket 均不挂载。
3. 模型通过结构化 `shell` tool 检查、写入和执行命令。完整 tool result 成为后续 turn。
4. 模型停止调用 tool 时视为提交；控制器用预先声明的命令运行公开 pytest，并在执行前后校验完整 workspace。除 `editable_paths` 声明的实现文件外，任何路径变化都会使该轮失败。
5. 每轮提交复制为 `attempts/attempt-N/`，后续修复不覆盖旧快照。
6. Agent 完全停止后，独立 verifier 容器才以只读方式挂载 attempt workspace 和隐藏测试目录，分别验证首轮和最终快照。
7. 隐藏输出只写实验日志和结果，不再触发模型修复。

## 4. 安全不变量

- 候选代码不得直接在宿主 Python 中执行。
- 运行时必须使用 `--network none`、`--read-only`、`--cap-drop ALL`、`no-new-privileges`、CPU/内存/PID 限额和有限 `/tmp` tmpfs。
- Agent 容器不传入宿主环境变量；只设置显式的 Python/pytest 运行变量。
- 修改、新增或删除受保护测试都使公开 verifier 失败，即使 pytest exit code 为 0。
- 新增、删除或修改 `editable_paths` 之外的文件或目录同样使公开 verifier 失败。
- `doctor` 未通过时不运行真实候选代码。

## 5. 指标

每次 run 保留：首次/最终公开通过、首次/最终隐藏通过、超时、隐藏功能回归、测试文件违规、实际模型调用数、prompt/completion/total token 和模型延迟。

benchmark 可用固定随机 seed 打乱“重复 × 策略 × 题目”的执行顺序，并在一份报告中跨重复聚合。聚合时按策略计算：

- 首次与最终隐藏测试通过率；
- 最终公开测试通过率；
- 超时率；
- 隐藏功能回归率（首次隐藏通过、最终隐藏失败）；
- 隐藏提升率（首次隐藏失败、最终隐藏通过）；
- 最终公开与最终隐藏通过率差距；
- 保护测试违规率；
- workspace 策略违规率；
- 模型调用数、token 和延迟的总量与均值；
- 每个成功 run 消耗的 token。

货币成本不用可能过期的价格表推测，因此默认为 `null`。需要货币成本时，应在实验配置中锁定当日价格版本再由原始 token 重算。

## 6. 演示案例

`public-pass-hidden-fail` 的错误实现只会分割普通空格。它能通过 5 个公开测试，但不能处理连续空格、制表符、换行和 Unicode 空白。因公开测试已通过，Agent 不会获得隐藏失败后的修复机会，这正好展示了为什么验收不能只报告公开 pytest。
