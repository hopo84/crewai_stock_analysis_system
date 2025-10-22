#!/usr/bin/env python3
"""
DeepSeek模型使用示例
演示如何在CrewAI股票分析系统中使用DeepSeek模型
"""
import os
import sys
from dotenv import load_dotenv

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 加载环境变量
load_dotenv()

from src.config.model_config import (
    ModelConfigManager,
    get_model_provider,
    get_model_info,
    validate_model_config,
    get_chat_llm,
    get_coder_llm
)


def demonstrate_model_switching():
    """演示模型切换功能"""
    print("=" * 60)
    print("CrewAI股票分析系统 - DeepSeek模型集成示例")
    print("=" * 60)

    # 显示当前模型配置
    print(f"\n📊 当前模型提供商: {get_model_provider()}")
    print(f"📋 模型配置信息:")
    model_info = get_model_info()
    for key, value in model_info.items():
        if 'key' not in key.lower():  # 不显示API密钥
            print(f"   {key}: {value}")

    # 验证模型配置
    print(f"\n🔍 配置验证结果: {'✅ 通过' if validate_model_config() else '❌ 失败'}")

    return True


def demonstrate_llm_creation():
    """演示LLM实例创建"""
    print("\n" + "=" * 60)
    print("LLM实例创建演示")
    print("=" * 60)

    try:
        # 创建聊天模型
        print("\n🤖 创建聊天模型...")
        chat_llm = get_chat_llm()
        print(f"✅ 聊天模型创建成功: {type(chat_llm).__name__}")

        # 如果是DeepSeek提供商，还可以创建代码模型
        if get_model_provider() == 'deepseek':
            print("\n💻 创建代码模型...")
            coder_llm = get_coder_llm()
            print(f"✅ 代码模型创建成功: {type(coder_llm).__name__}")
        else:
            print("\n💻 当前提供商不支持专门的代码模型，使用聊天模型")

    except Exception as e:
        print(f"❌ LLM创建失败: {str(e)}")
        return False

    return True


def demonstrate_crew_usage():
    """演示在Crew中使用模型"""
    print("\n" + "=" * 60)
    print("Crew使用演示")
    print("=" * 60)

    try:
        from src.crews.analysis_crew import AnalysisCrew

        print("\n🏢 创建分析团队...")
        analysis_crew = AnalysisCrew()

        print(f"✅ 分析团队创建成功")
        print(f"📊 团队使用的模型提供商: {get_model_provider()}")

        # 注意：这里只是演示创建，不执行实际分析
        print("💡 提示: 团队已准备就绪，可以进行股票分析")

    except ImportError as e:
        print(f"⚠️  导入分析团队失败: {str(e)}")
        print("   这可能是因为缺少某些依赖包")
        return False
    except Exception as e:
        print(f"❌ 创建分析团队失败: {str(e)}")
        return False

    return True


def show_environment_setup():
    """显示环境设置指南"""
    print("\n" + "=" * 60)
    print("环境设置指南")
    print("=" * 60)

    current_provider = os.getenv('MODEL_PROVIDER', 'openai')

    print(f"\n当前设置: MODEL_PROVIDER={current_provider}")

    if current_provider == 'deepseek':
        print("\n🚀 DeepSeek模型配置:")
        print("   ✅ 已启用DeepSeek模型")
        print("   📋 请确保以下环境变量已正确设置:")
        print("      - DEEPSEEK_API_KEY")
        print("      - DEEPSEEK_CHAT_MODEL (可选)")
        print("      - DEEPSEEK_CODER_MODEL (可选)")
        print("      - DEEPSEEK_BASE_URL (可选)")
    else:
        print("\n🔄 切换到DeepSeek模型:")
        print("   1. 在.env文件中设置: MODEL_PROVIDER=deepseek")
        print("   2. 配置DEEPSEEK_API_KEY")
        print("   3. 重新运行此示例")

    print("\n💰 成本优势:")
    if current_provider == 'deepseek':
        print("   ✅ 正在使用DeepSeek，享受更低的API成本")
    else:
        print("   💡 切换到DeepSeek可以显著降低API调用成本")

    print("\n🌏 中文支持:")
    if current_provider == 'deepseek':
        print("   ✅ DeepSeek对中文处理更优秀")
    else:
        print("   💡 DeepSeek在中文股票分析方面表现更佳")


def main():
    """主函数"""
    print("开始DeepSeek模型集成演示...")

    # 1. 演示模型切换
    if not demonstrate_model_switching():
        print("❌ 模型切换演示失败")
        return

    # 2. 演示LLM创建
    if not demonstrate_llm_creation():
        print("❌ LLM创建演示失败")
        return

    # 3. 演示Crew使用
    if not demonstrate_crew_usage():
        print("⚠️  Crew使用演示部分失败，但这可能是正常的")

    # 4. 显示环境设置指南
    show_environment_setup()

    print("\n" + "=" * 60)
    print("✅ DeepSeek模型集成演示完成!")
    print("💡 现在您可以使用DeepSeek模型进行股票分析了")
    print("=" * 60)


if __name__ == "__main__":
    main()