#!/usr/bin/env python3
"""
DeepSeek模型集成演示脚本
快速演示如何使用DeepSeek模型进行股票分析
"""
import os
import sys
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    print("🚀 CrewAI股票分析系统 - DeepSeek模型集成演示")
    print("=" * 60)

    # 检查当前模型配置
    try:
        from src.config.model_config import (
            get_model_provider,
            get_model_info,
            validate_model_config
        )

        provider = get_model_provider()
        print(f"\n📊 当前模型提供商: {provider}")

        if provider == 'deepseek':
            print("✅ DeepSeek模型已启用!")
            print("💰 享受更低的API成本")
            print("🇨🇳 更好的中文支持")
        else:
            print("ℹ️ 当前使用OpenAI模型")
            print("💡 要切换到DeepSeek，请设置: MODEL_PROVIDER=deepseek")

        # 显示模型配置
        model_info = get_model_info()
        print(f"\n📋 模型配置:")
        print(f"   聊天模型: {model_info.get('chat_model', 'N/A')}")
        print(f"   管理模型: {model_info.get('manager_model', 'N/A')}")
        if model_info.get('coder_model'):
            print(f"   代码模型: {model_info['coder_model']}")
        print(f"   最大令牌: {model_info.get('max_tokens', 'N/A')}")
        print(f"   温度参数: {model_info.get('temperature', 'N/A')}")

        # 验证配置
        config_valid = validate_model_config()
        print(f"\n🔍 配置验证: {'✅ 通过' if config_valid else '❌ 失败'}")

        if not config_valid:
            print("\n⚠️ 配置验证失败，请检查:")
            if provider == 'deepseek':
                print("   - DEEPSEEK_API_KEY 是否已设置")
                print("   - API密钥格式是否正确")
            else:
                print("   - OPENAI_API_KEY 是否已设置")
                print("   - API密钥格式是否正确")

    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        print("请确保项目依赖已正确安装")
        return

    except Exception as e:
        print(f"❌ 配置检查失败: {e}")
        return

    # 演示模型切换
    print(f"\n" + "=" * 60)
    print("🔄 模型切换演示")
    print("=" * 60)

    print("\n💡 切换到DeepSeek模型:")
    print("   1. 在 .env 文件中设置: MODEL_PROVIDER=deepseek")
    print("   2. 配置 DEEPSEEK_API_KEY=your-api-key")
    print("   3. 重新运行此脚本")

    print("\n💡 切换回OpenAI模型:")
    print("   1. 在 .env 文件中设置: MODEL_PROVIDER=openai")
    print("   2. 确保 OPENAI_API_KEY 已配置")
    print("   3. 重新运行此脚本")

    # 显示使用示例
    print(f"\n" + "=" * 60)
    print("📝 使用示例")
    print("=" * 60)

    print("\n🔧 在代码中使用:")
    print("""
from src.config.model_config import get_chat_llm, get_coder_llm

# 获取聊天模型
chat_llm = get_chat_llm()

# 获取代码模型（DeepSeek独有）
coder_llm = get_coder_llm()
""")

    print("\n🏢 在股票分析中使用:")
    print("""
from src.crews.analysis_crew import AnalysisCrew

# 创建分析团队（自动使用配置的模型）
crew = AnalysisCrew()

# 执行分析
result = crew.execute_collaborative_analysis(
    company="平安银行",
    ticker="000001.SZ"
)
""")

    # 显示下一步操作
    print(f"\n" + "=" * 60)
    print("🎯 下一步操作")
    print("=" * 60)

    print("\n📚 了解更多:")
    print("   - 查看: docs/DeepSeek模型集成指南.md")
    print("   - 运行: python examples/deepseek_usage_example.py")
    print("   - 测试: python test_deepseek_integration.py")

    print("\n🚀 开始分析:")
    print("   - 配置好API密钥后即可开始股票分析")
    print("   - DeepSeek模型特别适合中文股票分析场景")

    print(f"\n" + "=" * 60)
    print("✨ 演示完成！感谢使用DeepSeek模型集成功能")
    print("=" * 60)

if __name__ == "__main__":
    main()