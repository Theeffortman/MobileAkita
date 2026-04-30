# Honor Agent 系统架构文档

> 本文档描述当前 MVP 的真实架构。项目目标是多智能体自进化协作平台，当前已经具备可运行 API、Web 控制台、Android 客户端、多 Agent 顺序编排、GitHub Intelligence 和进化评估引擎。

---

## 系统概览

Honor Agent 当前采用单服务架构。FastAPI 是唯一后端入口，Web 控制台、Android APK、Python SDK 和 REST 调用都连接到同一套 HTTP API。

```txt
Client Layer
  Web Console     Android APK     Python SDK     REST/cURL
       │              │              │              │
       └──────────────┴──────────────┴──────────────┘
                              │
                              ▼
FastAPI Server
  server.py
  - serve static Web console
  - expose health, task, agent, GitHub APIs
  - keep MVP task state in memory
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
Multi-Agent Orchestrator  GitHub Intelligence  Evolution Engine
orchestrator.py           github_intelligence.py evolution.py
          │                   │                   │
          └───────────────────┴───────────────────┘
                              │
                              ▼
Data Models
  models.py
```

---

## 模块职责

| 模块 | 文件 | 职责 |
|------|------|------|
| API 服务 | `src/honor_agent/server.py` | 注册 FastAPI 路由、托管 Web 控制台、维护任务/结果/进化报告内存表 |
| 数据模型 | `src/honor_agent/models.py` | 定义 Task、AgentInfo、AgentRun、OrchestrationResult、EvolutionReport、GitHubRepoInsight、ApiResponse |
| 多 Agent 编排器 | `src/honor_agent/orchestrator.py` | 顺序执行 Agent，传递上下文，记录每一步输入、输出和 handoff |
| 进化评估引擎 | `src/honor_agent/evolution.py` | 根据执行轨迹生成评分、风险、优势和下一步改进建议 |
| GitHub Intelligence | `src/honor_agent/github_intelligence.py` | 解析仓库 URL、读取 GitHub 元数据、生成健康分和维护建议 |
| Python SDK | `src/honor_agent/client.py` | 给 Python 调用方提供任务、Agent、GitHub 分析和进化报告查询能力 |
| Web 控制台 | `src/honor_agent/static/` | 无构建依赖的浏览器操作界面 |
| Android 客户端 | `android/` | 原生 Java APK，连接后端执行健康检查、仓库分析和任务演示 |

---

## 请求生命周期

### 创建任务

```txt
Client
  │
  ▼
POST /api/v1/tasks
  │
  ▼
TaskCreate -> Task
  │
  ▼
TASKS[task_id] = Task
```

### 运行多 Agent 任务

```txt
Client
  │
  ▼
POST /api/v1/tasks/{task_id}/run
  │
  ▼
Task.status = running
  │
  ▼
orchestrate_task(task, AGENTS)
  │
  ├── data_analyst
  │     input: original task context
  │     output: analysis findings
  │
  ├── report_generator
  │     input: data_analyst output
  │     output: structured report
  │
  └── github_intelligence
        input: report_generator output
        output: repository maintenance plan
  │
  ▼
build_evolution_report(orchestration_result)
  │
  ▼
TASK_RESULTS[task_id] = TaskResult
EVOLUTION_REPORTS[task_id] = EvolutionReport
  │
  ▼
ApiResponse(TaskResult)
```

---

## 多 Agent 编排模型

当前编排策略是 `sequential`。每个 Agent 执行后，输出会进入 `context.latest_output`，下一个 Agent 的 `input_summary` 会引用上一个 Agent 的摘要。

### AgentRun

每一步运行都会保存：

| 字段 | 说明 |
|------|------|
| `agent_id` | 执行的 Agent ID |
| `agent_name` | Agent 显示名称 |
| `status` | `completed` / `skipped` / `failed` |
| `input_summary` | 当前 Agent 接收到的上游上下文摘要 |
| `output` | 当前 Agent 的结构化输出 |
| `started_at` / `completed_at` | 时间戳 |

### OrchestrationResult

最终编排结果包含：

| 字段 | 说明 |
|------|------|
| `strategy` | 当前为 `sequential` |
| `agent_count` | 实际执行或跳过的步骤数 |
| `runs` | 每个 Agent 的运行记录 |
| `final_output.agent_sequence` | Agent 执行顺序 |
| `final_output.handoffs` | Agent 之间的上下文交接 |
| `final_output.latest_output` | 最后一个 Agent 输出 |
| `evolution` | 进化评估报告 |

---

## 进化评估模型

进化评估引擎读取 `OrchestrationResult`，为每次运行生成 `EvolutionReport`。

### 当前评分信号

| 信号 | 影响 |
|------|------|
| Agent 步骤完成 | 提高单 Agent 分数 |
| 输出包含 `summary` | 提高可读性评分 |
| 输出包含 `handoff` | 提高协作连续性评分 |
| 存在 skipped Agent | 记录风险并生成修复建议 |
| 缺少运行记录 | 记录为高风险 |

### EvolutionReport

| 字段 | 说明 |
|------|------|
| `overall_score` | 总体评分 |
| `readiness` | `needs_attention` / `usable` / `strong` |
| `strengths` | 运行优势 |
| `risks` | 风险项 |
| `recommended_next_actions` | 下一步改进建议 |
| `agent_reports` | 每个 Agent 的评分和建议 |

---

## 当前内置 Agent

| Agent ID | 职责 | 输出 |
|----------|------|------|
| `data_analyst` | 读取任务参数，形成数据分析发现 | `summary`, `findings`, `handoff` |
| `report_generator` | 读取上游发现，生成结构化报告 | `summary`, `report`, `handoff` |
| `github_intelligence` | 读取上游报告和仓库 URL，形成维护建议 | `summary`, `repository`, `recommendations`, `handoff` |

---

## 状态存储

当前 MVP 使用进程内字典保存状态：

| 存储 | 内容 |
|------|------|
| `TASKS` | 已创建任务 |
| `TASK_RESULTS` | 最近一次任务运行结果 |
| `EVOLUTION_REPORTS` | 最近一次进化评估报告 |

服务重启后这些数据会清空。生产版本应替换为 SQLite、PostgreSQL 或其他持久化存储。

---

## 扩展方向

下一阶段建议按这个顺序进化：

1. 增加持久化数据库，保存任务、运行记录和进化报告。
2. 把确定性 Agent 函数替换为真实 LLM / 工具执行器。
3. 增加工作流 DAG，支持并行执行、失败重试和条件分支。
4. 增加认证授权、API Key 管理、审计日志。
5. 让 Evolution Engine 读取历史报告，自动推荐工作流模板和 Agent 参数优化。
6. 接入 GitHub Issue / PR 自动创建能力，让仓库维护建议变成真实行动。

---

## 相关文档

- [API 文档](./API_DOCS.md)
- [部署指南](./DEPLOYMENT.md)
- [Android 部署指南](./ANDROID.md)
