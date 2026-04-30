# Honor Agent

> 多智能体自进化 AI 协作平台 - 让 AI 助手成为您的数字员工团队

<p align="center">
  <img src="https://img.shields.io/badge/Version-0.1.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/Platform-Cross--Platform-green.svg" alt="Platform">
  <img src="https://img.shields.io/badge/License-MIT-orange.svg" alt="License">
  <img src="https://img.shields.io/badge/Python-3.10+-yellow.svg" alt="Python">
  <img src="https://img.shields.io/badge/Agents-50+-purple.svg" alt="Agents">
</p>

<p align="center">
  <a href="https://github.com/Theeffortman/HonorAgent/actions">
    <img src="https://github.com/Theeffortman/HonorAgent/workflows/CI/badge.svg" alt="CI">
  </a>
  <a href="https://github.com/Theeffortman/HonorAgent/releases">
    <img src="https://img.shields.io/github/release/Theeffortman/HonorAgent.svg" alt="Release">
  </a>
  <img src="https://img.shields.io/badge/status-MVP-blue?style=flat" alt="Status">
</p>

---

## 📖 项目简介

Honor Agent 是一款**多智能体自进化 AI 协作平台**，通过模拟人类操作实现各类应用自动化控制，让用户以自然语言指令驱动 AI 助手完成复杂任务。

**核心理念**：`AI 协作自动化，让工作更智能`

当前仓库已经从概念文档升级为可运行的 MVP：包含 FastAPI 后端、Python SDK、Web 可视化控制台、GitHub 仓库智能分析、Android 客户端和 GitHub Actions 自动打包流程。

### 核心优势

| 优势 | 说明 |
|------|------|
| 🤖 **多 Agent 协作入口** | 通过统一任务模型把不同 Agent 组合进同一个任务 |
| 🧠 **仓库智能分析** | 读取 GitHub 仓库元数据，生成健康分、风险点和维护建议 |
| 🔌 **Web + Android 双端** | Web 控制台用于桌面管理，Android APK 用于移动端操作 |
| 🎯 **开箱即用 API** | 安装后即可启动 FastAPI 服务并调用任务、Agent 和 GitHub 分析接口 |
| 🔒 **本地优先** | 默认任务数据保存在进程内，方便本地开发和二次扩展 |

---

## ✨ 功能特性

### ✅ 当前已实现

| 功能 | 说明 | 入口 |
|------|------|------|
| **Web 可视化控制台** | 在浏览器里完成健康检查、Agent 查看、任务创建、任务运行和 GitHub 分析 | `http://localhost:8000/` |
| **任务管理 API** | 支持创建任务、列出任务、查看任务详情、运行任务 | `/api/v1/tasks` |
| **Agent 能力中心** | 内置 Data Analyst、Report Generator、GitHub Intelligence 三类 Agent 元数据 | `/api/v1/agents` |
| **GitHub Intelligence** | 分析 GitHub 仓库，输出健康分、风险信号、正向信号和建议任务 | `/api/v1/github/analyze` |
| **Python SDK** | 通过 `HonorAgent` 客户端调用任务和 GitHub 分析能力 | `src/honor_agent/client.py` |
| **Android 客户端** | 原生 Android App，可连接后端、分析仓库、创建并运行演示任务 | `android/` |
| **自动化测试** | pytest 覆盖 API、SDK、GitHub 分析和 Web 控制台入口 | `tests/` |
| **CI / APK 打包** | GitHub Actions 自动运行测试并构建 debug APK | `.github/workflows/` |

### 🖥️ Web 可视化控制台

控制台随后端服务一起启动，不需要单独安装 Node.js 或前端构建工具。打开 `http://localhost:8000/` 后可以完成：

- 检查后端服务是否在线。
- 查看当前可用 Agent 和每个 Agent 的能力标签。
- 创建任务并选择参与任务的 Agent。
- 查看任务列表、任务详情和任务状态。
- 一键运行任务并查看执行结果。
- 输入 GitHub 仓库地址，生成仓库健康分析结果。
- 查看最近一次 API 响应日志，方便调试。

### 🧩 后端 API

Honor Agent 后端基于 FastAPI，当前提供一套最小但完整的任务编排接口：

| 接口 | 方法 | 功能 |
|------|------|------|
| `/health` | `GET` | 服务健康检查 |
| `/api/v1/agents` | `GET` | 获取可用 Agent 列表 |
| `/api/v1/tasks` | `POST` | 创建任务 |
| `/api/v1/tasks` | `GET` | 获取任务列表 |
| `/api/v1/tasks/{task_id}` | `GET` | 获取任务详情 |
| `/api/v1/tasks/{task_id}/run` | `POST` | 运行任务 |
| `/api/v1/github/analyze` | `POST` | 分析 GitHub 仓库 |

### 📱 Android APK

Android 客户端是原生 Java 实现，主要用于移动端连接 Honor Agent 后端。当前支持：

- 配置 API Base URL 和 API Key。
- 检查后端健康状态。
- 输入 GitHub 仓库地址并触发智能分析。
- 创建并运行演示任务。
- 在手机端直接查看 JSON 响应结果。

APK 可以通过 GitHub Actions 的 `Android APK` workflow 自动构建。构建完成后下载 `honor-agent-debug-apk` artifact，解压即可得到 `app-debug.apk`。

### 🧠 GitHub Intelligence

GitHub Intelligence 是项目当前的核心扩展能力之一。它会解析仓库 URL，并在允许远程访问时读取 GitHub 仓库元数据，然后生成：

- 仓库基础信息。
- 健康分 `health_score`。
- 正向信号 `signals`。
- 风险项 `risks`。
- 可执行维护建议 `suggested_tasks`。
- 原始元数据摘要 `metadata`。

这个能力可以作为后续“自动维护仓库 Agent”的入口，例如自动补 README、补 License、检查 CI、生成 Issue、规划重构任务等。

### 🔧 核心模块

| 模块 | 描述 |
|------|------|
| **任务编排核心** | 用统一 Task 模型描述任务名称、描述、Agent、参数、优先级和状态 |
| **Agent 注册中心** | 暴露可用 Agent 的 ID、名称、描述和能力标签 |
| **执行模拟器** | 当前 MVP 可将任务从 `created` 推进到 `completed` 并返回执行摘要 |
| **GitHub 分析器** | 把 GitHub 仓库元数据转成健康分和维护建议 |
| **Web 控制台** | 提供无需前端构建的浏览器操作界面 |
| **移动端客户端** | Android App 连接同一套后端 API |

### 🗺️ 规划中的能力

| 功能 | 说明 |
|------|------|
| **持久化存储** | 将当前内存任务存储升级为 SQLite / PostgreSQL |
| **真实 Agent 执行器** | 接入 LLM、工具调用、浏览器控制、文件操作等真实执行能力 |
| **权限系统** | API Key、用户、角色、审计日志和操作授权 |
| **工作流编排** | 支持多步骤 DAG、并行执行、失败重试和结果聚合 |
| **知识库能力** | 接入文档索引、RAG 检索和长期记忆 |
| **自动仓库维护** | 基于 GitHub Intelligence 自动创建 Issue、PR 和修复建议 |

---

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           Honor Agent 系统架构                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                        用户交互层 (UI Layer)                     │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐         │   │
│  │  │  Web UI │  │  CLI   │  │   API   │  │  Mobile │         │   │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘         │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                    │                                    │
│                                    ▼                                    │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                      业务编排层 (Orchestration Layer)            │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │   │
│  │  │  协作引擎   │  │  工作流引擎 │  │  知识引擎   │           │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘           │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                    │                                    │
│                                    ▼                                    │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                        Agent 核心层 (Agent Core Layer)          │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │   │
│  │  │  进化引擎   │  │  动作引擎   │  │  反思引擎   │           │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘           │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │   │
│  │  │  改进引擎   │  │  优化引擎   │  │  告警引擎   │           │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘           │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 快速开始

### 环境要求

| 组件 | 最低要求 | 推荐配置 |
|------|----------|----------|
| **Python** | 3.10+ | 3.11+ |
| **内存** | 4GB | 8GB+ |
| **磁盘** | 2GB | 10GB+ |
| **PostgreSQL** | 13+ | 15+ |
| **Redis** | 6+ | 7+ |

### 📦 安装部署

#### 方式一：Docker 部署（推荐）

```bash
# 克隆项目
git clone https://github.com/Theeffortman/HonorAgent.git
cd HonorAgent

# 快速启动
docker-compose up -d

# 查看服务状态
docker-compose ps
```

#### 方式二：本地开发

```bash
# 1. 克隆项目
git clone https://github.com/Theeffortman/HonorAgent.git
cd HonorAgent

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate

# 3. 安装依赖
pip install -e ".[dev]"

# 4. 配置环境变量
cp .env.example .env
# 编辑 .env 填入你的 API Keys

# 5. 启动服务
honor-agent
```

服务启动后打开可视化控制台：

```txt
http://localhost:8000/
```

控制台包含健康检查、Agent 列表、任务创建、任务列表、任务详情、任务运行和 GitHub 仓库分析。

### ⚙️ 配置说明

编辑 `.env` 文件配置必要参数：

```bash
# 数据库配置
DATABASE_URL=postgresql://user:password@localhost:5432/honor_agent
REDIS_URL=redis://localhost:6379/0

# 安全配置（必填，生产环境必须修改）
SECRET_KEY=your-secret-key-at-least-32-characters-long
JWT_SECRET=your-jwt-secret-key

# AI 服务配置
OPENAI_API_KEY=sk-your-openai-api-key
```

### ✅ 验证安装

```bash
# 健康检查
curl http://localhost:8000/health
```

### Android APK

仓库包含原生 Android 客户端：

```txt
android/
```

本地构建：

```bash
cd android
gradle :app:assembleDebug
```

也可以通过 GitHub Actions 的 `Android APK` workflow 自动构建并下载 `app-debug.apk`。

详细部署和使用步骤见 [Android 部署指南](./docs/ANDROID.md)。

---

## 📡 API 使用示例

### Python SDK

```python
from honor_agent import HonorAgent

client = HonorAgent(api_key="your-api-key")

task = client.tasks.create(
    name="数据分析任务",
    description="分析销售数据并生成报告",
    agents=["data_analyst"]
)

result = client.tasks.run(task_id=task.id)
print(result.output)
```

### REST API

```bash
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Authorization: Bearer your-api-key" \
  -d '{"name": "数据分析任务", "agents": ["data_analyst"]}'
```

### GitHub Intelligence

```bash
curl -X POST http://localhost:8000/api/v1/github/analyze \
  -H "Content-Type: application/json" \
  -d '{"url": "https://github.com/Theeffortman/HonorAgent", "include_remote": true}'
```

该能力会把 GitHub 仓库元数据转成健康分、风险信号和可执行任务建议，可作为后续多 Agent 自动维护仓库的入口。

---

## 📂 项目结构

```
HonorAgent/
├── README.md                      # 项目总览
├── docs/                          # 技术文档
│   ├── ARCHITECTURE.md           # 系统架构文档
│   ├── API_DOCS.md               # API 接口文档
│   ├── DEPLOYMENT.md             # 部署指南
│   ├── CONTRIBUTING.md           # 贡献指南
│   └── CHANGELOG.md              # 更新日志
├── src/honor_agent/              # Python SDK 与最小 API 服务
│   ├── client.py                 # 异步 SDK 客户端
│   ├── github_intelligence.py    # GitHub 仓库分析能力
│   ├── models.py                 # Pydantic 数据模型
│   ├── server.py                 # FastAPI 应用
│   └── static/                   # Web 可视化控制台
├── android/                      # 原生 Android APK 客户端
├── tests/                        # 自动化测试
├── .github/workflows/            # CI 配置
├── examples/                     # 示例代码
│   ├── python/
│   └── javascript/
└── deploy/                       # 部署配置
```

---

## 📊 项目统计

| 指标 | 数值 |
|------|------|
| **可运行 API** | FastAPI MVP |
| **Python 包** | `honor_agent` |
| **Web 控制台** | 内置静态控制台 |
| **Android APK** | GitHub Actions 自动打包 |
| **测试** | pytest |

---

## ❓ 常见问题

### Q: 如何获取 API Key？

A: 配置环境变量 `OPENAI_API_KEY` 或其他 AI 服务密钥。

### Q: 支持哪些 AI 模型？

A: 支持 OpenAI GPT-4、Claude、MiniMax、阿里云通义千问等多种模型。

### Q: 如何扩展自定义 Agent？

A: 继承 `BaseAgent` 类并实现 `execute` 方法，详见架构文档。

---

## 🤝 贡献指南

我们欢迎所有形式的贡献！请阅读 [CONTRIBUTING.md](./docs/CONTRIBUTING.md) 了解更多。

---

## 📜 开源协议

本项目采用 [MIT 许可证](./LICENSE)。

---

<p align="center">
  <strong>Honor Agent - 让 AI 协作更简单</strong>
</p>
