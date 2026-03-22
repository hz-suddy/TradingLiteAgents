# 使用DeepSeek模型指南

本文档说明如何在TradingAgents中使用DeepSeek模型。

## 快速开始

### 1. 获取DeepSeek API Key

1. 访问 https://platform.deepseek.com
2. 注册账户并登录
3. 在控制面板中获取你的API Key
4. 保存API Key用于下一步

### 2. 配置环境变量

**方式一：使用 .env 文件（推荐）**

```bash
# 复制示例文件
cp .env.example .env

# 编辑 .env 文件，添加你的DeepSeek API Key
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxx
```

**方式二：直接设置环境变量**

```bash
export DEEPSEEK_API_KEY=sk-xxxxxxxxxxxx
```

### 3. 修改代码配置

编辑 `main.py`，修改配置：

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 创建配置，指定使用DeepSeek
config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "deepseek"
config["deep_think_llm"] = "deepseek-chat"      # 或使用推理模型 "deepseek-reasoner"
config["quick_think_llm"] = "deepseek-chat"

# 其他配置保持不变
ta = TradingAgentsGraph(debug=True, config=config)

# 运行分析
_, decision = ta.propagate("NVDA", "2024-05-10")
print(decision)
```

## DeepSeek 可用模型

### deepseek-chat
- **类型**: 基础对话模型
- **参数**: 671B
- **用途**: 快速推理和分析
- **速度**: 快
- **成本**: 相对低

### deepseek-reasoner
- **类型**: 推理模型 (类似OpenAI o1)
- **参数**: 671B
- **用途**: 复杂分析和深度思考
- **速度**: 较慢
- **成本**: 相对高

## 推荐配置

### 配置1：平衡方案（推荐）
```python
config["llm_provider"] = "deepseek"
config["deep_think_llm"] = "deepseek-reasoner"    # 深度分析用推理模型
config["quick_think_llm"] = "deepseek-chat"      # 快速任务用基础模型
config["max_debate_rounds"] = 2                   # 多轮辩论以获得更好分析
```

### 配置2：成本优化方案
```python
config["llm_provider"] = "deepseek"
config["deep_think_llm"] = "deepseek-chat"
config["quick_think_llm"] = "deepseek-chat"
config["max_debate_rounds"] = 1                   # 减少轮数降低成本
```

### 配置3：深度推理方案
```python
config["llm_provider"] = "deepseek"
config["deep_think_llm"] = "deepseek-reasoner"
config["quick_think_llm"] = "deepseek-reasoner"
config["max_debate_rounds"] = 2
```

## 高级配置

如需自定义API端点（例如使用代理或本地部署）：

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
from tradingagents.llm_clients import create_llm_client

config = DEFAULT_CONFIG.copy()

# 使用自定义base_url
custom_deep_client = create_llm_client(
    provider="deepseek",
    model="deepseek-chat",
    base_url="https://your-custom-api.com/v1",  # 自定义端点
    api_key="your-api-key",
    timeout=30,  # 自定义超时
)

ta = TradingAgentsGraph(debug=True, config=config)
ta.deep_thinking_llm = custom_deep_client.get_llm()
```

## API 定价信息

访问 https://platform.deepseek.com 查看最新定价。

| 模型 | 输入 | 输出 |
|-----|------|------|
| deepseek-chat | $0.14/1M tokens | $0.28/1M tokens |
| deepseek-reasoner | $0.55/1M tokens | $2.19/1M tokens |

（注：以上价格仅作参考，请以官网最新价格为准）

## 常见问题

### Q1: 如何切换回OpenAI模型？
```python
config["llm_provider"] = "openai"
config["deep_think_llm"] = "gpt-5.2"
config["quick_think_llm"] = "gpt-5-mini"
```

### Q2: DeepSeek模型需要多长时间才能获得结果？
- `deepseek-chat`: 通常 20-60 秒
- `deepseek-reasoner`: 通常 1-5 分钟（因为进行深度推理）

### Q3: 可以同时使用多个LLM提供商吗？
可以！创建多个`TradingAgentsGraph`实例，分别配置不同的提供商。

### Q4: API连接超时怎么办？
添加自定义超时参数：
```python
custom_client = create_llm_client(
    provider="deepseek",
    model="deepseek-chat",
    timeout=60  # 增加到60秒
)
```

### Q5: 如何调试API连接问题？
启用debug模式并查看错误信息：
```python
ta = TradingAgentsGraph(debug=True, config=config)
```

## 支持

如遇到问题：
1. 确认API Key有效：访问 https://platform.deepseek.com 检查余额
2. 检查网络连接
3. 查看错误日志（启用debug模式）
4. 访问 https://discord.com/invite/hk9PGKShPK 获取社区支持
