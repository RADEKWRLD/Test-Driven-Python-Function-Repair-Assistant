# 本机 WSL 环境验收记录

本文保留精简前的环境与 API 实测事实。当前实现范围以 README 和 EXPERIMENT_PROTOCOL.md 为准；精简后的回归验收记录见本文末尾。

日期：2026-10-30。运行方案：本机 WSL Ubuntu + Docker Desktop Linux 引擎 + DeepSeek API。

| 项目 | 实际检查结果 |
| --- | --- |
| WSL 发行版 | Ubuntu-22.04，WSL2，运行中 |
| Linux 用户 | mamba，UID/GID 为 1000 |
| Docker Desktop / Engine | 4.63.0 / 29.2.1，Ubuntu 可连接 |
| 原有 Python | 系统 Python 3.10.12；mambaunet 环境为 3.10.12，均保留 |
| 项目 Python | 项目内独立 CPython 3.12.16 |
| 项目虚拟环境 | `.venv/`（Linux 环境，不能当作 Windows 虚拟环境运行） |
| 沙箱镜像 | `function-repair/sandbox-python:dev`，本轮构建成功，镜像 ID 前缀 `91529e8dde76` |
| WSL 资源观察 | 内存 6.6 GiB、swap 2.0 GiB；项目所在 E 盘检查时剩余约 49 GiB |

## 已执行的最小验收

1. `.venv/bin/repair-agent doctor`：通过，输出 `Sandbox image: ready`。
2. `make check`：Ruff 格式/lint、mypy 通过；44 项非 Docker 开发测试通过。
3. `make sandbox-test`：1 项真实 Docker 集成测试通过，不调用模型 API。

Docker 集成测试使用预先编写的固定提交，验证修复控制器、只读挂载和公开/隐藏评测链路。原生 Windows 的两个 UID/GID 兼容错误在 Ubuntu 下不出现。

没有执行 50 题正式实验，也没有将环境测试结果作为模型修复成功率。

## DeepSeek 最小测试准备

- 项目 `.env` 已配置本地密钥，模型设置为 `deepseek-flash`，单次输出上限 2048 token，模型请求超时 120 秒。密钥不写入文档或事件日志。
- DeepSeek 适配器显式设置 `thinking.type=disabled`，保持单次调用提交代码和 temperature=0 的现有协议，并有对应单元测试。
- 原因：当前官方 API 默认启用思考模式，不能依赖旧版服务默认值。参考：[官方思考模式说明](https://api-docs.deepseek.com/guides/thinking_mode/)。
- 最小测试脚本为 `var/environment/minimal_api_check.py`：仅使用 chunk-list 一道演示题和三组 1/3/3 预算，最多 7 次模型调用；出现服务或基础设施错误即停止。
- 脚本先检查模型列表和账号可用状态，再记录实际 token、模型延迟、整题耗时及调用前后余额差。余额差可能受延迟入账或同账号其他请求影响，不能代替最终账单；零差额也不证明免费。
- 已完成最小 API 测试：三组均首次通过，实际调用 3 次、合计 2497 token，完整流程 21.349 秒。余额差显示 0.00 元，不代表免费。详见 [最小接入测试结果](MINIMAL_API_CHECK.md)。

## 后续使用

先打开 Docker Desktop，保持引擎运行。在 Ubuntu 终端执行：

```bash
cd /mnt/e/Python函数修复助手/Test-Driven-Python-Function-Repair-Assistant
.venv/bin/repair-agent doctor

# 仅在填好项目 .env 后执行最小 API 检查
.venv/bin/python var/environment/minimal_api_check.py
```

不需要重新安装 Ubuntu 或复用 mambaunet 环境。现有虚拟环境直接使用 `.venv/bin/...` 即可，无需依赖系统 Python 3.10 或手动激活环境。默认 `make experiment` 会启动 50 题三组一轮正式实验（150 个 run），环境验收时不执行。

## 精简后回归验收

按最新精简要求，默认 `make experiment` 已改为 **50 题、三组、一轮，共 150 个 run**，不再默认运行三轮；本轮没有执行该命令。

在原 Ubuntu/Python/Docker 环境复核：doctor、Ruff 格式/lint、mypy 均通过；39 项开发测试、1 项 Docker 集成测试全部通过。已删除的下载导入、自动拆分等外围测试不再计数。普通日志、四图 Markdown 报告和简单结果保存/跳过机制已由对应开发测试验证，MLX-LM 适配器及安全约束仍保留。

本轮没有新的 DeepSeek 调用、费用或正式实验结果。历史最小 API 结果保持不变；当前具体操作以 [精简操作手册](OPERATIONS.md) 为准。
