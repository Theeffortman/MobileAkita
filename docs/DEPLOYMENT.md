# Honor Agent 部署指南

> 本文档详细介绍 Honor Agent 的各种部署方式。

---

## 📋 目录

- [环境准备](#环境准备)
- [Docker 部署](#docker-部署)
- [本地开发部署](#本地开发部署)
- [Kubernetes 部署](#kubernetes-部署)
- [生产环境配置](#生产环境配置)

---

## 环境准备

### 系统要求

| 组件 | 最低要求 | 推荐配置 |
|------|----------|----------|
| CPU | 2 核 | 4 核+ |
| 内存 | 4 GB | 8 GB+ |
| 磁盘 | 20 GB | 50 GB+ |
| 操作系统 | Ubuntu 20.04+ / CentOS 8+ | Ubuntu 22.04 LTS |

### 必需软件

```bash
python3 --version  # >= 3.10
docker --version   # >= 20.10
docker-compose --version  # >= 2.0
```

---

## Docker 部署

### 快速启动

```bash
# 1. 克隆项目
git clone https://github.com/Theeffortman/HonorAgent.git
cd HonorAgent

# 2. 创建环境配置文件
cp .env.example .env
# 编辑 .env 填入必要配置

# 3. 启动服务
docker-compose up -d

# 4. 查看服务状态
docker-compose ps

# 5. 查看日志
docker-compose logs -f
```

### Docker Compose 配置

```yaml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: honor_agent
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### 启动完整版（含监控）

```bash
docker-compose --profile monitoring up -d

# 访问
# - API: http://localhost:8000
# - Prometheus: http://localhost:9090
# - Grafana: http://localhost:3000
```

---

## 本地开发部署

### 1. 克隆代码

```bash
git clone https://github.com/Theeffortman/HonorAgent.git
cd HonorAgent
```

### 2. 创建虚拟环境

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

### 3. 安装依赖

```bash
pip install -e ".[dev]"
```

### 4. 配置环境变量

```bash
cp .env.example .env
nano .env
```

### 5. 运行服务

```bash
# 开发模式
uvicorn honor_agent.server:app --reload

# 生产模式
honor-agent
```

### 6. 验证安装

```bash
curl http://localhost:8000/health
```

---

## Kubernetes 部署

### Helm 安装

```bash
# 添加 Helm 仓库
helm repo add honor-agent https://charts.honoragent.com
helm repo update

# 安装
helm install honor-agent honor-agent/honor-agent \
  --namespace honor-agent \
  --set api.replicas=2
```

### 生产配置

```yaml
# values-production.yaml
api:
  replicaCount: 3
  resources:
    requests:
      memory: "512Mi"
      cpu: "500m"
    limits:
      memory: "2Gi"
      cpu: "2000m"
```

---

## 生产环境配置

### 环境变量配置

```bash
NODE_ENV=production
DATABASE_URL=postgresql://user:pass@db:5432/honor_agent
REDIS_URL=redis://redis:6379/0
SECRET_KEY=<随机生成的32位密钥>
JWT_SECRET=<随机生成的32位密钥>
OPENAI_API_KEY=<your-key>
LOG_LEVEL=info
```

### 反向代理配置 (Nginx)

```nginx
upstream honor_api {
    server 127.0.0.1:8000;
    keepalive 32;
}

server {
    listen 80;
    server_name api.honoragent.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.honoragent.com;

    ssl_certificate /etc/ssl/certs/honor_agent.crt;
    ssl_certificate_key /etc/ssl/private/honor_agent.key;

    location / {
        proxy_pass http://honor_api;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 📚 相关文档

- [架构文档](./ARCHITECTURE.md)
- [API 文档](./API_DOCS.md)
