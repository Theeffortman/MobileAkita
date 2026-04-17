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
