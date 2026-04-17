# Honor Agent API 文档

> 本文档提供 Honor Agent RESTful API 的完整参考。

---

## 基础信息

### Base URL

```
生产环境: https://api.honoragent.com/v1
本地开发: http://localhost:8000/api/v1
```

### 响应格式

```json
{
  "success": true,
  "data": { ... },
  "message": "操作成功",
  "request_id": "req_abc123"
}
```

---

## 认证

### 获取 Access Token

```http
POST /auth/token
Content-Type: application/json

{
  "api_key": "your-api-key",
  "api_secret": "your-api-secret"
}
```

---

## 任务管理

### 创建任务

```http
POST /api/v1/tasks
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "数据分析任务",
  "description": "分析销售数据并生成周报",
  "agents": ["data_analyst", "report_generator"],
  "params": {
    "data_source": "sales_db"
  },
  "priority": "normal"
}
```

**参数说明**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | 是 | 任务名称 |
| description | string | 否 | 任务描述 |
| agents | array | 是 | 使用的 Agent 列表 |
| params | object | 否 | 任务参数 |
| priority | string | 否 | 优先级：low/normal/high/critical |

### 获取任务详情

```http
GET /api/v1/tasks/{task_id}
Authorization: Bearer {token}
```

### 触发任务执行

```http
POST /api/v1/tasks/{task_id}/run
Authorization: Bearer {token}
```

### 列出任务

```http
GET /api/v1/tasks?page=1&page_size=20&status=completed
Authorization: Bearer {token}
```

---

## Agent 管理

### 列出 Agent

```http
GET /api/v1/agents
Authorization: Bearer {token}
```

### 获取 Agent 详情

```http
GET /api/v1/agents/{agent_id}
Authorization: Bearer {token}
```

### 创建自定义 Agent

```http
POST /api/v1/agents
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "my_agent",
  "description": "我的自定义 Agent",
  "capabilities": ["task_1", "task_2"],
  "config": {
    "model": "gpt-4",
    "temperature": 0.7
  }
}
```

---

## 工作流

### 创建工作流

```http
POST /api/v1/workflows
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "数据处理流水线",
  "steps": [
    {"name": "采集", "agent": "data_collector"},
    {"name": "清洗", "agent": "data_cleaner"},
    {"name": "分析", "agent": "data_analyst"}
  ]
}
```

### 执行工作流

```http
POST /api/v1/workflows/{workflow_id}/run
Authorization: Bearer {token}
```

---

## 知识库

### 上传文档

```http
POST /api/v1/knowledge/documents
Authorization: Bearer {token}
Content-Type: multipart/form-data

file: (binary)
collection: "my_knowledge_base"
```

### 搜索知识库

```http
POST /api/v1/knowledge/search
Authorization: Bearer {token}
Content-Type: application/json

{
  "query": "如何配置系统参数",
  "collection": "my_knowledge_base",
  "top_k": 5
}
```

---

## 错误码

| 错误码 | HTTP 状态 | 说明 |
|--------|-----------|------|
| INVALID_REQUEST | 400 | 请求参数错误 |
| UNAUTHORIZED | 401 | 未授权或 Token 过期 |
| NOT_FOUND | 404 | 资源不存在 |
| RATE_LIMITED | 429 | 请求频率超限 |
| INTERNAL_ERROR | 500 | 服务器内部错误 |

---

## SDK 下载

| 语言 | 包管理器 | 命令 |
|------|----------|------|
| Python | pip | `pip install honor-agent` |
| JavaScript | npm | `npm install @honor-agent/sdk` |

---

## 📚 相关文档

- [架构文档](./ARCHITECTURE.md)
- [部署指南](./DEPLOYMENT.md)
