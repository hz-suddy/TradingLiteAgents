#!/usr/bin/env python3
"""验证DeepSeek集成是否完整"""

import os
import sys
from pathlib import Path

def check_files():
    """检查必要的文件是否存在"""
    print("\n📁 文件检查:")
    print("=" * 60)
    
    files_to_check = [
        ("tradingagents/llm_clients/deepseek_client.py", "DeepSeekClient文件"),
        (".env", ".env配置文件"),
        ("main_deepseek.py", "示例脚本"),
        ("requirements.txt", "依赖文件"),
    ]
    
    all_exist = True
    for filepath, desc in files_to_check:
        if Path(filepath).exists():
            print(f"✅ {desc:20} - {filepath}")
        else:
            print(f"❌ {desc:20} - {filepath} 不存在")
            all_exist = False
    
    return all_exist

def check_env_vars():
    """检查环境变量"""
    print("\n🔑 环境变量检查:")
    print("=" * 60)
    
    api_key = os.environ.get("DEEPSEEK_API_KEY", "").strip()
    
    if api_key and api_key.startswith("sk-"):
        print(f"✅ DEEPSEEK_API_KEY 已设置")
        print(f"   Key长度: {len(api_key)} 字符")
        print(f"   前缀: {api_key[:10]}...")
        return True
    elif api_key:
        print(f"⚠️  DEEPSEEK_API_KEY 已设置但格式可能不正确")
        print(f"   当前值: {api_key[:20]}...")
        return False
    else:
        print(f"❌ DEEPSEEK_API_KEY 未设置")
        return False

def check_imports():
    """检查Python导入"""
    print("\n📦 导入检查:")
    print("=" * 60)
    
    checks = [
        ("tradingagents.llm_clients", "create_llm_client"),
        ("tradingagents.llm_clients.deepseek_client", "DeepSeekClient"),
        ("tradingagents.graph.trading_graph", "TradingAgentsGraph"),
        ("tradingagents.default_config", "DEFAULT_CONFIG"),
    ]
    
    all_ok = True
    for module, item in checks:
        try:
            mod = __import__(module, fromlist=[item])
            getattr(mod, item)
            print(f"✅ {module}.{item}")
        except ImportError as e:
            print(f"❌ {module}.{item} - {str(e)[:50]}")
            all_ok = False
        except AttributeError:
            print(f"❌ {module}.{item} - 属性不存在")
            all_ok = False
    
    return all_ok

def check_client_creation():
    """检查是否可以创建DeepSeek客户端"""
    print("\n🔌 客户端创建检查:")
    print("=" * 60)
    
    try:
        from tradingagents.llm_clients import create_llm_client
        
        client = create_llm_client(
            provider="deepseek",
            model="deepseek-chat"
        )
        print(f"✅ DeepSeekClient 创建成功")
        print(f"   类型: {type(client).__name__}")
        
        llm = client.get_llm()
        print(f"✅ LLM实例创建成功")
        print(f"   模型: {llm.model_name}")
        
        return True
    except Exception as e:
        print(f"❌ 客户端创建失败: {str(e)[:100]}")
        return False

def main():
    """主验证函数"""
    print("\n" + "=" * 60)
    print("🔍 DeepSeek 集成验证")
    print("=" * 60)
    
    results = {
        "文件存在": check_files(),
        "环境变量": check_env_vars(),
        "导入成功": check_imports(),
        "客户端创建": check_client_creation(),
    }
    
    print("\n" + "=" * 60)
    print("📊 验证总结:")
    print("=" * 60)
    
    for check_name, passed in results.items():
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{check_name:15} {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ 所有检查通过！可以运行 main_deepseek.py")
        print("=" * 60)
        return 0
    else:
        print("❌ 有一些检查未通过，请检查上面的错误")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    sys.exit(main())
