# DeepSeek快速开始 (30秒版本)

## 1️⃣ 获取API Key
访问 https://platform.deepseek.com → 复制你的API Key

## 2️⃣ 配置
```bash
# 编辑.env文件
nano .env

# 添加一行：
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxx
```

## 3️⃣ 编辑main.py

只需要改这三行：
```python
config["llm_provider"] = "deepseek"
config["deep_think_llm"] = "deepseek-reasoner"
config["quick_think_llm"] = "deepseek-chat"
```

## 4️⃣ 运行
```bash
python main.py
```

---

## 或直接用示例脚本（完全相同的配置）
```bash
python main_deepseek.py
```

---

## 三种配置对比

| 配置 | 深度 | 速度 | 成本 | 场景 |
|------|------|------|------|------|
| **chat** | ⭐ | 🚀🚀 | 💰 | 快速分析 |
| **reasoner** | ⭐⭐⭐ | 🚀 | 💰💰💰 | 精准分析 |
| **mixed** (推荐) | ⭐⭐⭐ | 🚀🚀 | 💰💰 | 平衡方案 |

---

## 支持的模型

- `deepseek-chat` - 快速通用模型
- `deepseek-reasoner` - 深度推理模型

---

## 遇到问题？

| 问题 | 解决 |
|------|------|
| API Key错误 | 检查.env文件中的DEEPSEEK_API_KEY |
| 连接超时 | 检查网络，或增加timeout参数 |
| 模型不存在 | 使用`deepseek-chat`或`deepseek-reasoner` |
| 余额不足 | 访问https://platform.deepseek.com充值 |

---

## 成本估算

假设分析1只股票，使用平衡方案(mixed)：
- 平均cost: ~$0.10-0.50 per stock
- 1000只股票: ~$100-500

---

## 更多信息

- 详细指南: `DEEPSEEK_SETUP.md`
- 修改总结: `DEEPSEEK_CHANGES.md`
- 示例代码: `main_deepseek.py`

---

✅ 完成！现在可以开始使用DeepSeek了。
