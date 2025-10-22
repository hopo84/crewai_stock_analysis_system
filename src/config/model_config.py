"""
模型配置管理器
统一管理OpenAI、DeepSeek等多种LLM模型的配置和创建
"""
import logging
import os
from typing import Dict, Any, Optional, Union
from enum import Enum

logger = logging.getLogger(__name__)


class ModelProvider(Enum):
    """模型提供商枚举"""
    OPENAI = "openai"
    DEEPSEEK = "deepseek"


class ModelType(Enum):
    """模型类型枚举"""
    CHAT = "chat"
    CODER = "coder"
    MANAGER = "manager"
    PLANNING = "planning"


class ModelConfigManager:
    """模型配置管理器"""

    def __init__(self):
        self.provider = self._get_model_provider()
        self.config = self._load_model_config()

    def _get_model_provider(self) -> ModelProvider:
        """获取当前配置的模型提供商"""
        provider = os.getenv('MODEL_PROVIDER', 'openai').lower()

        if provider == 'deepseek':
            return ModelProvider.DEEPSEEK
        elif provider == 'openai':
            return ModelProvider.OPENAI
        else:
            logger.warning(f"未知的模型提供商: {provider}，使用默认的OpenAI")
            return ModelProvider.OPENAI

    def _load_model_config(self) -> Dict[str, Any]:
        """加载模型配置"""
        if self.provider == ModelProvider.DEEPSEEK:
            return self._load_deepseek_config()
        else:
            return self._load_openai_config()

    def _load_openai_config(self) -> Dict[str, Any]:
        """加载OpenAI配置"""
        return {
            'chat_model': os.getenv('OPENAI_CHAT_MODEL', 'gpt-4o-mini'),
            'manager_model': os.getenv('OPENAI_MANAGER_MODEL', 'gpt-4o-mini'),
            'planning_model': os.getenv('OPENAI_PLANNING_MODEL', 'gpt-4o-mini'),
            'api_key': os.getenv('OPENAI_API_KEY'),
            'base_url': os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1'),
            'max_tokens': int(os.getenv('OPENAI_MAX_TOKENS', '4000')),
            'temperature': float(os.getenv('OPENAI_TEMPERATURE', '0.7')),
        }

    def _load_deepseek_config(self) -> Dict[str, Any]:
        """加载DeepSeek配置"""
        return {
            'chat_model': os.getenv('DEEPSEEK_CHAT_MODEL', 'deepseek-chat'),
            'coder_model': os.getenv('DEEPSEEK_CODER_MODEL', 'deepseek-coder'),
            'manager_model': os.getenv('DEEPSEEK_MANAGER_MODEL', 'deepseek-chat'),
            'planning_model': os.getenv('DEEPSEEK_PLANNING_MODEL', 'deepseek-chat'),
            'api_key': os.getenv('DEEPSEEK_API_KEY'),
            'base_url': os.getenv('DEEPSEEK_BASE_URL', 'https://api.deepseek.com/v1'),
            'max_tokens': int(os.getenv('DEEPSEEK_MAX_TOKENS', '4000')),
            'temperature': float(os.getenv('DEEPSEEK_TEMPERATURE', '0.7')),
            'top_p': float(os.getenv('DEEPSEEK_TOP_P', '0.95')),
        }

    def create_llm(self, model_type: ModelType = ModelType.CHAT, **kwargs):
        """
        创建LLM实例

        Args:
            model_type: 模型类型
            **kwargs: 额外的模型参数

        Returns:
            LLM实例
        """
        try:
            try:
                from crewai import LLM
            except ImportError:
                logger.warning("无法导入 crewai.LLM，返回模型名称字符串")
                return self._get_model_name(model_type)

            if self.provider == ModelProvider.DEEPSEEK:
                return self._create_deepseek_llm(model_type, LLM, **kwargs)
            else:
                return self._create_openai_llm(model_type, LLM, **kwargs)

        except Exception as e:
            logger.error(f"创建LLM实例失败: {str(e)}")
            # 降级到返回模型名称字符串
            return self._get_model_name(model_type)

    def _create_openai_llm(self, model_type: ModelType, LLM, **kwargs):
        """创建OpenAI LLM实例"""
        # 根据模型类型选择模型名称
        if model_type == ModelType.MANAGER:
            model_name = self.config['manager_model']
        elif model_type == ModelType.PLANNING:
            model_name = self.config['planning_model']
        else:
            model_name = self.config['chat_model']

        # 构建模型配置
        model_config = {
            'model': f"openai/{model_name}",
            'api_key': self.config['api_key'],
            'base_url': self.config['base_url'],
            'max_tokens': self.config['max_tokens'],
            'temperature': self.config['temperature'],
            **kwargs
        }

        logger.info(f"创建OpenAI LLM: {model_name}")
        return LLM(**model_config)

    def _create_deepseek_llm(self, model_type: ModelType, LLM, **kwargs):
        """创建DeepSeek LLM实例"""
        # 根据模型类型选择模型名称
        if model_type == ModelType.CODER:
            model_name = self.config['coder_model']
        elif model_type == ModelType.MANAGER:
            model_name = self.config['manager_model']
        elif model_type == ModelType.PLANNING:
            model_name = self.config['planning_model']
        else:
            model_name = self.config['chat_model']

        # 构建模型配置
        model_config = {
            'model': model_name,  # DeepSeek API直接使用模型名称，不需要前缀
            'api_key': self.config['api_key'],
            'base_url': self.config['base_url'],
            'max_tokens': self.config['max_tokens'],
            'temperature': self.config['temperature'],
            'top_p': self.config.get('top_p', 0.95),
            **kwargs
        }

        logger.info(f"创建DeepSeek LLM: {model_name}")
        return LLM(**model_config)

    def _get_model_name(self, model_type: ModelType) -> str:
        """获取模型名称字符串（降级方案）"""
        if self.provider == ModelProvider.DEEPSEEK:
            if model_type == ModelType.CODER:
                return self.config['coder_model']
            elif model_type == ModelType.MANAGER:
                return self.config['manager_model']
            elif model_type == ModelType.PLANNING:
                return self.config['planning_model']
            else:
                return self.config['chat_model']
        else:
            if model_type == ModelType.MANAGER:
                return self.config['manager_model']
            elif model_type == ModelType.PLANNING:
                return self.config['planning_model']
            else:
                return self.config['chat_model']

    def get_manager_llm(self, **kwargs):
        """获取管理者LLM"""
        return self.create_llm(ModelType.MANAGER, **kwargs)

    def get_planning_llm(self, **kwargs):
        """获取规划LLM"""
        return self.create_llm(ModelType.PLANNING, **kwargs)

    def get_chat_llm(self, **kwargs):
        """获取聊天LLM"""
        return self.create_llm(ModelType.CHAT, **kwargs)

    def get_coder_llm(self, **kwargs):
        """获取代码LLM（仅DeepSeek支持）"""
        if self.provider != ModelProvider.DEEPSEEK:
            logger.warning("代码专用模型仅DeepSeek支持，使用聊天模型替代")
            return self.get_chat_llm(**kwargs)
        return self.create_llm(ModelType.CODER, **kwargs)

    def validate_config(self) -> bool:
        """验证模型配置"""
        try:
            api_key = self.config.get('api_key')
            if not api_key or api_key.startswith('your-'):
                logger.error(f"{self.provider.value} API密钥未配置或为占位符")
                return False

            # 验证API密钥格式（根据提供商不同）
            if self.provider == ModelProvider.OPENAI and not api_key.startswith('sk-'):
                logger.warning(f"{self.provider.value} API密钥格式可能不正确，OpenAI密钥通常以'sk-'开头")
            elif self.provider == ModelProvider.DEEPSEEK and not api_key.startswith('sk-'):
                logger.warning(f"{self.provider.value} API密钥格式可能不正确，DeepSeek密钥通常以'sk-'开头")

            # 验证基础URL
            base_url = self.config.get('base_url')
            if not base_url or not base_url.startswith('http'):
                logger.error(f"{self.provider.value} 基础URL格式不正确")
                return False

            logger.info(f"{self.provider.value} 模型配置验证通过")
            return True

        except Exception as e:
            logger.error(f"模型配置验证失败: {str(e)}")
            return False

    def get_current_provider(self) -> str:
        """获取当前模型提供商"""
        return self.provider.value

    def get_model_info(self) -> Dict[str, Any]:
        """获取模型信息"""
        return {
            'provider': self.provider.value,
            'chat_model': self.config.get('chat_model'),
            'manager_model': self.config.get('manager_model'),
            'planning_model': self.config.get('planning_model'),
            'coder_model': self.config.get('coder_model'),
            'base_url': self.config.get('base_url'),
            'max_tokens': self.config.get('max_tokens'),
            'temperature': self.config.get('temperature'),
        }


# 全局模型配置管理器实例 - 延迟初始化
_model_config_manager = None


def _get_model_config_manager():
    """获取模型配置管理器实例，支持延迟初始化"""
    global _model_config_manager
    if _model_config_manager is None:
        _model_config_manager = ModelConfigManager()
    return _model_config_manager


def get_manager_llm(**kwargs):
    """便捷函数：获取管理者LLM"""
    return _get_model_config_manager().get_manager_llm(**kwargs)


def get_planning_llm(**kwargs):
    """便捷函数：获取规划LLM"""
    return _get_model_config_manager().get_planning_llm(**kwargs)


def get_chat_llm(**kwargs):
    """便捷函数：获取聊天LLM"""
    return _get_model_config_manager().get_chat_llm(**kwargs)


def get_coder_llm(**kwargs):
    """便捷函数：获取代码LLM"""
    return _get_model_config_manager().get_coder_llm(**kwargs)


def validate_model_config() -> bool:
    """便捷函数：验证模型配置"""
    return _get_model_config_manager().validate_config()


def get_model_provider() -> str:
    """便捷函数：获取当前模型提供商"""
    return _get_model_config_manager().get_current_provider()


def get_model_info() -> Dict[str, Any]:
    """便捷函数：获取模型信息"""
    return _get_model_config_manager().get_model_info()


# For backward compatibility
model_config_manager = _get_model_config_manager