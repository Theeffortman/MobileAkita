# Honor Agent API 文档

> 本文档只描述当前仓库已经实现并通过测试的 API。规划中的能力会单独标注，避免把未实现接口误当成可用功能。

---

## 基础信息

### Base URL

```txt
本地开发: http://localhost:8000
API 前缀: http://localhost:8000/api/v1
Web 控制台: http://localhost:8000/
```

### 响应格式

所有业务 API 使用统一响应结构：

```json
{
  "success": true,
  "data": {},
  "message": "操作成功",
  "request_id": "req_abc123"
}
```

### 当前认证状态

当前 MVP 版本不会强制校验 `Authorization`。SDK 会自动发送 `Bearer {api_key}`，用于和未来认证系统保持兼容。

---

## 健康检查

```http
GET /health
```

响应：

```json
{
  "status": "ok",
  "service": "honor-agent"
}
```

---

## Web 控制台

```http
GET /
GET /static/app.css
GET /static/app.js
```

控制台能力：

- 查看 API 健康状态。
- 查看 Agent 列表。
- 创建任务。
- 运行多 Agent 任务。
- 查看最近一次 API 响应日志。
- 发起 GitHub 仓库分析。

---

## 任务管理

### 创建任务

```http
POST /api/v1/tasks
Content-Type: application/json

{
  "name": "多智能体分析任务",
  "description": "分析销售数据，生成报告，并输出仓库维护建议",
  "agents": ["data_analyst", "report_generator", "github_intelligence"],
  "params": {
    "data_source": "sales_db",
    "date_range": "last_week",
    "extra": {
      "github_url": "https://github.com/Theeffortman/HonorAgent"
    }
  },
  "priority": "high"
}
```

参数说明：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | string | 是 | 任务名称 |
| `description` | string | 否 | 任务描述 |
| `agents` | string[] | 否 | 执行任务的 Agent ID 列表；为空时默认使用第一个注册 Agent |
| `params.data_source` | string | 否 | 数据源描述 |
| `params.date_range` | string | 否 | 时间范围 |
| `params.extra.github_url` | string | 否 | 传给 GitHub Intelligence 的仓库地址 |
| `priority` | string | 否 | `low` / `normal` / `high` / `critical` |

### 列出任务

```http
GET /api/v1/tasks
```

当前版本返回内存中的全部任务，不支持分页和过滤。

### 获取任务详情

```http
GET /api/v1/tasks/{task_id}
```

### 运行任务

```http
POST /api/v1/tasks/{task_id}/run
```

运行后会触发顺序多 Agent 编排，并返回 `TaskResult`。`TaskResult.output` 是完整的 `OrchestrationResult`：

```json
{
  "task_id": "task_xxx",
  "status": "completed",
  "output": {
    "task_id": "task_xxx",
    "status": "completed",
    "strategy": "sequential",
    "agent_count": 3,
    "runs": [],
    "final_output": {},
    "evolution": {}
  }
}
```

### 获取最近一次任务结果

```http
GET /api/v1/tasks/{task_id}/result
```

任务未运行时返回 `404 Task result not found`。

### 获取进化评估报告

```http
GET /api/v1/tasks/{task_id}/evolution
```

任务未运行时返回 `404 Evolution report not found`。

`EvolutionReport` 包含：

| 字段 | 说明 |
|------|------|
| `overall_score` | 本次多 Agent 协作总体评分 |
| `readiness` | `needs_attention` / `usable` / `strong` |
| `strengths` | 本次运行优点 |
| `risks` | 本次运行风险 |
| `recommended_next_actions` | 下一步改进建议 |
| `agent_reports` | 每个 Agent 的单独评分和建议 |

---

## Agent 管理

### 列出 Agent

```http
GET /api/v1/agents
```

当前内置 Agent：

| Agent ID | 角色 | 能力 |
|----------|------|------|
| `data_analyst` | 数据分析 Agent | `analysis`, `reporting` |
| `report_generator` | 报告生成 Agent | `writing`, `summarization` |
| `github_intelligence` | GitHub 仓库智能 Agent | `repository-analysis`, `task-planning`, `risk-detection` |

---

## GitHub Intelligence

### 分析 GitHub 仓库

```http
POST /api/v1/github/analyze
Content-Type: application/json

{
  "url": "https://github.com/Theeffortman/HonorAgent",
  "include_remote": true
}
```

返回内容：

| 字段 | 说明 |
|------|------|
| `owner` | 仓库 owner |
| `repo` | 仓库名称 |
| `url` | 规范化 GitHub URL |
| `health_score` | 0-100 仓库健康分 |
| `signals` | 正向信号 |
| `risks` | 风险信号 |
| `suggested_tasks` | 可转成 HonorAgent 任务的建议 |
| `metadata` | GitHub API 返回的仓库元数据摘要 |

`include_remote=false` 时只解析 URL，不访问 GitHub API，适合离线测试。

---

## Python SDK

```python
from honor_agent import HonorAgent

client = HonorAgent(api_key="dev-api-key")

task = await client.tasks.create(
    name="多智能体分析任务",
    agents=["data_analyst", "report_generator", "github_intelligence"],
    params={
        "data_source": "sales_db",
        "date_range": "last_week",
        "extra": {"github_url": "https://github.com/Theeffortman/HonorAgent"},
    },
)

result = await client.tasks.run(task.id)
stored_result = await client.tasks.result(task.id)
evolution = await client.tasks.evolution(task.id)
insight = await client.github.analyze(
    "https://github.com/Theeffortman/HonorAgent",
    include_remote=False,
)
```

---

## 错误处理

当前常见错误：

| HTTP 状态 | 场景 |
|-----------|------|
| `400` | GitHub URL 非法 |
| `404` | 任务、任务结果或进化报告不存在 |
| `500` | 服务内部错误 |

---

## 规划中但尚未实现

以下能力是路线图，不属于当前可用 API：

- 用户登录和 Access Token 颁发。
- 创建、修改、删除自定义 Agent。
- 工作流 DAG API。
- 知识库上传和检索 API。
- 持久化数据库、队列、审计日志和权限系统。

---

## 相关文档

- [架构文档](./ARCHITECTURE.md)
- [部署指南](./DEPLOYMENT.md)
- [Android 部署指南](./ANDROID.md)
