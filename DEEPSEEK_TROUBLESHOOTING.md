# DeepSeek故障排查指南

遇到问题？按照本指南逐步排查。

---

## 问题1: "Unsupported LLM provider: deepseek"

### 症状
```
ValueError: Unsupported LLM provider: deepseek
```

### 原因
- factory.py中没有正确添加deepseek支持
- deepseek_client.py未被导入

### 解决步骤

1️⃣ **检查factory.py导入**
```bash
# 查看是否有导入语句
grep "deepseek_client" tradingagents/llm_clients/factory.py
```

✅ 应该看到：
```python
from .deepseek_client import DeepSeekClient
```

❌ 如果没有，添加该行

---

2️⃣ **检查factory函数逻辑**
```bash
grep -A 2 "deepseek" tradingagents/llm_clients/factory.py | grep -A 2 "provider_lower"
```

✅ 应该看到：
```python
if provider_lower == "deepseek":
    return DeepSeekClient(model, base_url, **kwargs)
```

❌ 如果没有，添加该分支

---

## 问题2: "DEEPSEEK_API_KEY not found"

### 症状
```
AuthenticationError: Invalid authentication
或
Error: API key not found
```

### 原因
- .env文件中未设置API Key
- API Key格式错误
- 环境变量未被加载

### 解决步骤

1️⃣ **验证.env文件**
```bash
# 检查.env文件是否存在
ls -la .env

# 检查内容
cat .env | grep DEEPSEEK
```

✅ 应该看到类似：
```
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxx
```

❌ 如果看不到或格式错误：
```bash
# 编辑.env
nano .env
# 添加一行：DEEPSEEK_API_KEY=sk-your-actual-key
```

---

2️⃣ **验证API Key格式**
```bash
# API Key应该以 sk- 开头
echo $DEEPSEEK_API_KEY | head -c 3
# 应该输出：sk-
```

❌ 如果不是 `sk-`，检查：
- 是否复制完整
- 是否包含多余空格
- 是否使用了错误的密钥

---

3️⃣ **验证环境变量加载**
```python
# 在main_deepseek.py顶部添加debug代码
from dotenv import load_dotenv
import os

load_dotenv()
print(f"API Key: {os.environ.get('DEEPSEEK_API_KEY', 'NOT FOUND')}")
```

✅ 应该输出：
```
API Key: sk-xxxxxxxxxxxxx
```

❌ 如果输出 `NOT FOUND`，检查：
- .env文件名是否正确（应该是 `.env` 不是 `.env.example`）
- 是否在项目根目录
- load_dotenv() 是否在其他导入之前

---

## 问题3: "Connection timeout"

### 症状
```
HTTPError: 408 Request Timeout
或
ConnectionError: timed out
```

### 原因
- 网络连接问题
- DeepSeek API服务器无响应
- 默认超时时间过短

### 解决步骤

1️⃣ **检查网络连接**
```bash
# 测试对DeepSeek API的连接
curl -I https://api.deepseek.com/v1
```

✅ 应该返回 `HTTP/1.1 200` 或 `HTTP/2 200`

❌ 如果无法连接：
- 检查VPN/代理设置
- 检查防火墙设置
- 尝试在浏览器访问 https://platform.deepseek.com

---

2️⃣ **增加超时时间**
```python
# main.py 或 main_deepseek.py
config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "deepseek"
config["deep_think_llm"] = "deepseek-chat"
config["quick_think_llm"] = "deepseek-chat"

# 创建客户端时增加超时
from tradingagents.llm_clients import create_llm_client

deep_client = create_llm_client(
    provider="deepseek",
    model="deepseek-chat",
    timeout=60  # 增加到60秒
)
```

---

3️⃣ **使用代理/VPN**

如果在某些地区无法直接访问DeepSeek:
```python
import httpx

# 创建自定义HTTP客户端
http_client = httpx.Client(
    proxy="http://your-proxy:port",
    timeout=60
)

deep_client = create_llm_client(
    provider="deepseek",
    model="deepseek-chat",
    http_client=http_client
)
```

---

## 问题4: "Model not found"

### 症状
```
NotFoundError: The model `deepseek-invalid` does not exist
```

### 原因
- 使用了不存在的模型名
- 模型名拼写错误

### 解决步骤

1️⃣ **检查支持的模型列表**
```bash
grep -A 5 "deepseek" tradingagents/llm_clients/validators.py
```

✅ 应该看到：
```python
"deepseek": [
    "deepseek-chat",
    "deepseek-reasoner",
],
```

---

2️⃣ **验证配置中的模型名**
```python
# main.py
config["deep_think_llm"] = "deepseek-chat"  # ✅ 正确
# 不要使用：
# config["deep_think_llm"] = "deepseek-chat-v1"  # ❌ 错误
# config["deep_think_llm"] = "deepseek_chat"     # ❌ 错误
```

---

## 问题5: "Insufficient balance"

### 症状
```
InsufficientQuotaError: Insufficient balance in account
或
No credits/balance
```

### 原因
- DeepSeek账户余额不足
- 超出API额度限制

### 解决步骤

1️⃣ **检查账户余额**
```
1. 访问 https://platform.deepseek.com
2. 登录账户
3. 进入"My Quota" 或 "Billing" 页面
4. 查看当前余额
```

---

2️⃣ **充值账户**
```
1. 在 https://platform.deepseek.com 充值
2. 选择充值金额并完成支付
3. 等待充值生效（通常5-10分钟）
```

---

3️⃣ **优化成本**
```python
# 使用成本更低的模型
config["deep_think_llm"] = "deepseek-chat"  # 比reasoner便宜
config["quick_think_llm"] = "deepseek-chat"
config["max_debate_rounds"] = 1  # 减少辩论轮数
```

---

## 问题6: "Invalid API key"

### 症状
```
AuthenticationError: Incorrect API key provided
或
Invalid API key format
```

### 原因
- API Key格式错误
- API Key已过期/被撤销
- 使用了错误账户的API Key

### 解决步骤

1️⃣ **重新生成API Key**
```
1. 访问 https://platform.deepseek.com/api_keys
2. 删除旧的API Key
3. 生成新的API Key
4. 复制完整的Key值（包括 sk- 前缀）
```

---

2️⃣ **验证Key格式**
```bash
# 检查Key长度（通常60-70字符）
echo $DEEPSEEK_API_KEY | wc -c

# 检查是否只包含字母、数字和 - 
echo $DEEPSEEK_API_KEY | grep -E '^sk-[a-zA-Z0-9]*$'
```

---

## 问题7: "Type or schema validation error"

### 症状
```
ValidationError: ...
或
JSON decode error
```

### 原因
- LangChain与DeepSeek API版本不兼容
- 模型参数不正确

### 解决步骤

1️⃣ **更新依赖**
```bash
# 升级langchain和langchain-openai
pip install --upgrade langchain langchain-openai

# 检查版本
pip list | grep langchain
```

✅ 应该使用较新版本（2024年3月之后）

---

2️⃣ **清理缓存并重新安装**
```bash
# 删除Python缓存
find . -type d -name __pycache__ -exec rm -r {} +
find . -type f -name "*.pyc" -delete

# 重新安装依赖
pip install -r requirements.txt
```

---

## 问题8: "Module not found"

### 症状
```
ModuleNotFoundError: No module named 'tradingagents.llm_clients.deepseek_client'
```

### 原因
- deepseek_client.py文件不存在
- Python path配置错误

### 解决步骤

1️⃣ **检查文件是否存在**
```bash
ls -la tradingagents/llm_clients/deepseek_client.py
```

❌ 如果文件不存在，重新创建：
```bash
# 从DEEPSEEK_QUICKSTART.md复制代码创建文件
# 或运行本指南的第一个问题解决方案
```

---

2️⃣ **检查Python路径**
```python
import sys
print(sys.path)
# 确保包含项目根目录
```

---

## 问题9: "Rate limit exceeded"

### 症状
```
RateLimitError: Rate limit exceeded
或
429 Too Many Requests
```

### 原因
- 调用API过于频繁
- 超过DeepSeek API限制

### 解决步骤

1️⃣ **添加请求延迟**
```python
import time

# 在分析多个股票时添加延迟
stocks = ["AAPL", "GOOGL", "MSFT"]
for stock in stocks:
    _, decision = ta.propagate(stock, "2024-05-10")
    print(decision)
    time.sleep(2)  # 等待2秒再发送下一个请求
```

---

2️⃣ **检查DeepSeek API限制**
```
访问 https://platform.deepseek.com/docs/api
查看当前账户的RateLimit配额
```

---

3️⃣ **考虑批量处理**
```python
# 而不是实时分析，考虑离线批量处理
# 这样可以更好地管理速率
```

---

## 问题10: "DeepSeekClient not defined"

### 症状
```
NameError: name 'DeepSeekClient' is not defined
```

### 原因
- 导入语句错误或缺失
- 模块初始化问题

### 解决步骤

1️⃣ **验证导入**
```bash
# 检查__init__.py中的导出
cat tradingagents/llm_clients/__init__.py
```

✅ 应该包含必要的导出（虽然不一定要导出DeepSeekClient）

---

2️⃣ **直接导入测试**
```python
# 在Python shell中测试
from tradingagents.llm_clients.deepseek_client import DeepSeekClient
print(DeepSeekClient)  # 应该输出类定义
```

❌ 如果报错，检查：
- 文件名是否正确
- 类名拼写是否正确
- 文件内容是否完整

---

## 快速诊断脚本

将以下代码保存为 `test_deepseek.py`，运行诊断：

```python
#!/usr/bin/env python3
"""DeepSeek集成诊断脚本"""

import sys
import os
from pathlib import Path

def check_file_exists(path, name):
    """检查文件是否存在"""
    if Path(path).exists():
        print(f"✅ {name} 存在")
        return True
    else:
        print(f"❌ {name} 不存在: {path}")
        return False

def check_env_var(var_name):
    """检查环境变量"""
    value = os.environ.get(var_name)
    if value:
        print(f"✅ {var_name} 已设置")
        return True
    else:
        print(f"❌ {var_name} 未设置")
        return False

def test_imports():
    """测试导入"""
    try:
        from tradingagents.llm_clients import create_llm_client
        print("✅ create_llm_client 导入成功")
    except ImportError as e:
        print(f"❌ create_llm_client 导入失败: {e}")
        return False
    
    try:
        from tradingagents.llm_clients.deepseek_client import DeepSeekClient
        print("✅ DeepSeekClient 导入成功")
    except ImportError as e:
        print(f"❌ DeepSeekClient 导入失败: {e}")
        return False
    
    return True

def main():
    print("=" * 60)
    print("DeepSeek 集成诊断")
    print("=" * 60)
    
    print("\n📁 文件检查:")
    check_file_exists("tradingagents/llm_clients/deepseek_client.py", "deepseek_client.py")
    check_file_exists(".env", ".env 文件")
    
    print("\n🔑 环境变量检查:")
    check_env_var("DEEPSEEK_API_KEY")
    
    print("\n📦 导入检查:")
    test_imports()
    
    print("\n✅ 诊断完成!")
    print("如有❌项目，参考本文档进行修复。")

if __name__ == "__main__":
    main()
```

运行诊断：
```bash
python test_deepseek.py
```

---

## 获取帮助

仍未解决？

1. 检查 `DEEPSEEK_SETUP.md` 的常见问题部分
2. 访问 DeepSeek 文档: https://platform.deepseek.com/docs
3. 加入社区: https://discord.com/invite/hk9PGKShPK
4. 检查GitHub Issues或创建新issue

---

## 成功指标

✅ 以下表示集成成功：

```bash
python main_deepseek.py
```

输出应包含：
- ✅ 市场分析报告
- ✅ 情绪分析报告  
- ✅ 新闻分析报告
- ✅ 基本面分析报告
- ✅ 最终交易决策

如果一切都显示，恭喜！🎉
