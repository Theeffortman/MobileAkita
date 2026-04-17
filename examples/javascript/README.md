# Honor Agent JavaScript/TypeScript SDK 示例

> 本目录包含 Honor Agent JavaScript/TypeScript SDK 的使用示例。

## 📋 示例列表

| 文件 | 说明 |
|------|------|
| `basic-task.ts` | 基础任务创建与执行 |

---

## 安装 SDK

```bash
npm install @honor-agent/sdk
# 或
yarn add @honor-agent/sdk
```

## 配置

```typescript
import { HonorAgent } from '@honor-agent/sdk';

const client = new HonorAgent({
  apiKey: process.env.HONOR_API_KEY!,
  baseUrl: process.env.HONOR_BASE_URL || 'http://localhost:8000',
});
```

## 示例: 基础任务

```typescript
/**
 * basic-task.ts - 基础任务创建与执行示例
 */
import { HonorAgent } from '@honor-agent/sdk';

async function main() {
  const client = new HonorAgent({
    apiKey: process.env.HONOR_API_KEY || 'your-api-key',
    baseUrl: process.env.HONOR_BASE_URL || 'http://localhost:8000',
  });

  try {
    const task = await client.tasks.create({
      name: '数据分析任务',
      description: '分析销售数据并生成周报',
      agents: ['data_analyst'],
      params: {
        dataSource: 'sales_db',
        dateRange: 'last_week',
      },
    });

    console.log(`✓ 任务创建成功: ${task.id}`);

    const result = await client.tasks.run({ taskId: task.id });

    console.log(`✓ 执行状态: ${result.status}`);
    if (result.output) {
      console.log(`✓ 输出:`, result.output);
    }

    return result;
  } catch (error) {
    console.error('任务执行失败:', error);
    throw error;
  }
}

main().catch(console.error);
```

## 运行示例

```bash
npm install
export HONOR_API_KEY="your-api-key"
npx ts-node basic-task.ts
```
