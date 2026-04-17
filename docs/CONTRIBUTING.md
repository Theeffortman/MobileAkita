# Honor Agent 贡献指南

> 感谢您对 Honor Agent 项目的兴趣！我们欢迎各种形式的贡献。

---

## 行为准则

我们承诺为所有参与者提供一个友好、安全和包容的环境。

### 我们的承诺

- 使用友好和包容的语言
- 尊重不同的观点和经验
- 优雅地接受建设性的批评
- 关注对社区最有利的事情
- 对其他社区成员表现出同理心

---

## 开始贡献

### 适合新手的任务

- 修复 Typo
- 完善文档
- 添加测试
- 翻译文档

标签参考：`good-first-issue`、`beginner`

### 贡献方式

| 方式 | 说明 |
|------|------|
| 🐛 Bug 修复 | 修复已知问题 |
| ✨ 新功能 | 添加新功能或模块 |
| 📖 文档 | 完善文档或添加示例 |
| 🔨 重构 | 优化代码结构 |
| 🧪 测试 | 添加或改进测试 |

---

## 开发环境

### 设置开发环境

```bash
# 1. Fork 仓库
# 点击 GitHub 页面右上角的 "Fork" 按钮

# 2. 克隆你的 Fork
git clone https://github.com/YOUR_USERNAME/HonorAgent.git
cd HonorAgent

# 3. 添加上游仓库
git remote add upstream https://github.com/Theeffortman/HonorAgent.git

# 4. 创建虚拟环境
python -m venv venv
source venv/bin/activate

# 5. 安装依赖
cd server
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 6. 安装预提交钩子
pre-commit install
```

---

## 开发流程

### 1. 创建功能分支

```bash
git checkout -b feature/your-feature-name
# 或
git checkout -b fix/issue-number
```

### 2. 进行开发并提交

```bash
git add .
git commit -m "feat: add new collaboration feature"
```

### 3. 推送分支

```bash
git push origin feature/your-feature-name
```

### 4. 创建 Pull Request

1. 访问你的 Fork 仓库
2. 点击 "Compare & pull request"
3. 填写 PR 描述
4. 关联相关 Issue
5. 提交 PR

---

## 代码规范

### Python 代码规范

```bash
# 格式化
black .
isort .

# 检查
ruff check .
```

### 提交信息格式

```
<type>(<scope>): <subject>

<body>
```

### Type 类型

| Type | 说明 |
|------|------|
| feat | 新功能 |
| fix | Bug 修复 |
| docs | 文档变更 |
| style | 代码格式 |
| refactor | 重构 |
| test | 测试相关 |

### 示例

```
feat(collaboration): add multi-agent team builder

- Add team_builder.py for dynamic team construction
- Implement task allocation algorithm
- Add result aggregation service

Closes #123
```

---

## 测试要求

### 测试覆盖要求

- 新功能必须有测试
- Bug 修复必须有回归测试
- 整体覆盖率应保持在 85% 以上

### 运行测试

```bash
pytest tests/ -v
pytest tests/test_collaboration.py -v
pytest tests/ --cov=server --cov-report=html
```

---

## 文档贡献

| 文档 | 位置 | 说明 |
|------|------|------|
| README | 根目录 | 项目总览 |
| API 文档 | docs/API.md | API 接口文档 |
| 架构文档 | docs/ARCHITECTURE.md | 系统架构 |
| 部署指南 | docs/DEPLOYMENT.md | 部署说明 |

---

## 反馈与问题

- 📖 阅读 [文档](../README.md)
- 🐛 提交 [Issue](https://github.com/Theeffortman/HonorAgent/issues)

---

感谢您的贡献！ 🎉
