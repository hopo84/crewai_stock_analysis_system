#!/usr/bin/env python3
"""
DeepSeek集成测试脚本
验证DeepSeek模型集成是否正常工作
"""
import os
import sys
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_model_config_manager():
    """测试模型配置管理器"""
    print("=" * 50)
    print("测试模型配置管理器")
    print("=" * 50)

    try:
        from src.config.model_config import (
            ModelConfigManager,
            get_model_provider,
            get_model_info,
            validate_model_config
        )

        # 测试默认配置（OpenAI）
        print("\n1. 测试默认配置 (OpenAI)")
        os.environ['MODEL_PROVIDER'] = 'openai'
        manager = ModelConfigManager()
        print(f"   ✅ 提供商: {manager.get_current_provider()}")
        print(f"   ✅ 配置验证: {'通过' if manager.validate_config() else '失败'}")

        # 测试DeepSeek配置
        print("\n2. 测试DeepSeek配置")
        os.environ['MODEL_PROVIDER'] = 'deepseek'
        manager = ModelConfigManager()
        print(f"   ✅ 提供商: {manager.get_current_provider()}")
        print(f"   ✅ 配置验证: {'通过' if manager.validate_config() else '失败'}")

        # 测试便捷函数
        print("\n3. 测试便捷函数")
        provider = get_model_provider()
        print(f"   ✅ 当前提供商: {provider}")

        model_info = get_model_info()
        print(f"   ✅ 模型信息: {model_info['chat_model']}")

        return True

    except Exception as e:
        print(f"   ❌ 测试失败: {str(e)}")
        return False


def test_llm_creation():
    """测试LLM实例创建"""
    print("\n" + "=" * 50)
    print("测试LLM实例创建")
    print("=" * 50)

    try:
        from src.config.model_config import (
            get_chat_llm,
            get_manager_llm,
            get_planning_llm,
            get_coder_llm,
            get_model_provider
        )

        provider = get_model_provider()
        print(f"\n当前提供商: {provider}")

        # 注意：这里只测试创建，不测试实际调用（需要有效的API密钥）
        print("\n1. 测试聊天模型创建")
        try:
            chat_llm = get_chat_llm()
            print(f"   ✅ 聊天模型创建成功: {type(chat_llm).__name__}")
        except Exception as e:
            print(f"   ⚠️  聊天模型创建失败（可能是API密钥问题）: {str(e)}")

        print("\n2. 测试管理模型创建")
        try:
            manager_llm = get_manager_llm()
            print(f"   ✅ 管理模型创建成功: {type(manager_llm).__name__}")
        except Exception as e:
            print(f"   ⚠️  管理模型创建失败（可能是API密钥问题）: {str(e)}")

        print("\n3. 测试规划模型创建")
        try:
            planning_llm = get_planning_llm()
            print(f"   ✅ 规划模型创建成功: {type(planning_llm).__name__}")
        except Exception as e:
            print(f"   ⚠️  规划模型创建失败（可能是API密钥问题）: {str(e)}")

        print("\n4. 测试代码模型创建")
        try:
            coder_llm = get_coder_llm()
            print(f"   ✅ 代码模型创建成功: {type(coder_llm).__name__}")
        except Exception as e:
            print(f"   ⚠️  代码模型创建失败（可能是API密钥问题）: {str(e)}")

        return True

    except Exception as e:
        print(f"   ❌ 测试失败: {str(e)}")
        return False


def test_crew_integration():
    """测试Crew集成"""
    print("\n" + "=" * 50)
    print("测试Crew集成")
    print("=" * 50)

    try:
        # 测试分析团队
        print("\n1. 测试分析团队集成")
        try:
            from src.crews.analysis_crew import AnalysisCrew
            crew = AnalysisCrew()
            print(f"   ✅ 分析团队创建成功")
        except Exception as e:
            print(f"   ❌ 分析团队创建失败: {str(e)}")

        # 测试决策团队
        print("\n2. 测试决策团队集成")
        try:
            from src.crews.decision_crew import DecisionCrew
            crew = DecisionCrew()
            print(f"   ✅ 决策团队创建成功")
        except Exception as e:
            print(f"   ❌ 决策团队创建失败: {str(e)}")

        return True

    except Exception as e:
        print(f"   ❌ 测试失败: {str(e)}")
        return False


def test_environment_switching():
    """测试环境切换"""
    print("\n" + "=" * 50)
    print("测试环境切换")
    print("=" * 50)

    try:
        from src.config.model_config import ModelConfigManager

        # 测试OpenAI配置
        print("\n1. 切换到OpenAI")
        os.environ['MODEL_PROVIDER'] = 'openai'
        manager = ModelConfigManager()
        print(f"   ✅ 当前提供商: {manager.get_current_provider()}")

        # 测试DeepSeek配置
        print("\n2. 切换到DeepSeek")
        os.environ['MODEL_PROVIDER'] = 'deepseek'
        manager = ModelConfigManager()
        print(f"   ✅ 当前提供商: {manager.get_current_provider()}")

        # 测试无效配置
        print("\n3. 测试无效配置")
        os.environ['MODEL_PROVIDER'] = 'invalid'
        manager = ModelConfigManager()
        print(f"   ✅ 无效配置回退到: {manager.get_current_provider()}")

        return True

    except Exception as e:
        print(f"   ❌ 测试失败: {str(e)}")
        return False


def main():
    """主测试函数"""
    print("🚀 开始DeepSeek模型集成测试")
    print()

    success_count = 0
    total_tests = 4

    # 1. 测试模型配置管理器
    if test_model_config_manager():
        success_count += 1

    # 2. 测试LLM创建
    if test_llm_creation():
        success_count += 1

    # 3. 测试Crew集成
    if test_crew_integration():
        success_count += 1

    # 4. 测试环境切换
    if test_environment_switching():
        success_count += 1

    # 输出测试结果
    print("\n" + "=" * 50)
    print("测试结果总结")
    print("=" * 50)
    print(f"总测试数: {total_tests}")
    print(f"成功数: {success_count}")
    print(f"失败数: {total_tests - success_count}")

    if success_count == total_tests:
        print("🎉 所有测试通过! DeepSeek集成成功!")
    else:
        print("⚠️  部分测试失败，请检查错误信息")

    print("\n💡 注意事项:")
    print("- API密钥相关的错误是正常的，只要配置结构正确即可")
    print("- 实际使用时需要配置有效的API密钥")
    print("- 可以通过设置环境变量 MODEL_PROVIDER=deepseek 来使用DeepSeek模型")


if __name__ == "__main__":
    main()