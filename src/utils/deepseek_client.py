"""
DeepSeek API客户端模块
提供DeepSeek API的集成功能，兼容OpenAI接口标准
"""
import logging
import os
import httpx
from typing import Dict, Any, Optional
from .http_utils import EnhancedHTTPClient

logger = logging.getLogger(__name__)


def create_deepseek_client() -> EnhancedHTTPClient:
    """
    创建配置了DeepSeek API的增强型HTTP客户端

    Returns:
        EnhancedHTTPClient: 配置好的HTTP客户端
    """
    # 从环境变量获取DeepSeek配置
    api_key = os.getenv('DEEPSEEK_API_KEY')
    base_url = os.getenv('DEEPSEEK_BASE_URL', 'https://api.deepseek.com/v1')

    if not api_key:
        logger.error("未设置DEEPSEEK_API_KEY环境变量")
        raise ValueError("未设置DEEPSEEK_API_KEY环境变量")

    # 设置请求头
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    # 创建并返回增强型HTTP客户端
    return EnhancedHTTPClient(
        max_retries=3,
        retry_backoff_factor=1.0,
        retry_statuses=(429, 500, 502, 503, 504),
        timeout=60,  # DeepSeek API可能需要较长时间
        headers=headers,
        base_url=base_url,
        # 增加连接池大小以支持并发请求
        limits=httpx.Limits(max_connections=100, max_keepalive_connections=20)
    )


def get_deepseek_model_config() -> Dict[str, Any]:
    """
    获取DeepSeek模型配置

    Returns:
        Dict[str, Any]: 模型配置字典
    """
    return {
        'chat_model': os.getenv('DEEPSEEK_CHAT_MODEL', 'deepseek-chat'),
        'coder_model': os.getenv('DEEPSEEK_CODER_MODEL', 'deepseek-coder'),
        'max_tokens': int(os.getenv('DEEPSEEK_MAX_TOKENS', '4000')),
        'temperature': float(os.getenv('DEEPSEEK_TEMPERATURE', '0.7')),
        'top_p': float(os.getenv('DEEPSEEK_TOP_P', '0.95')),
    }


def validate_deepseek_config() -> bool:
    """
    验证DeepSeek配置是否正确

    Returns:
        bool: 配置是否有效
    """
    try:
        api_key = os.getenv('DEEPSEEK_API_KEY')
        if not api_key:
            logger.error("DeepSeek API密钥未配置")
            return False

        if not api_key.startswith('sk-'):
            logger.warning("DeepSeek API密钥格式可能不正确，通常以'sk-'开头")

        # 检查基础URL配置
        base_url = os.getenv('DEEPSEEK_BASE_URL', 'https://api.deepseek.com/v1')
        if not base_url.startswith('http'):
            logger.error("DeepSeek基础URL格式不正确")
            return False

        logger.info("DeepSeek配置验证通过")
        return True

    except Exception as e:
        logger.error(f"DeepSeek配置验证失败: {str(e)}")
        return False


class DeepSeekModelFactory:
    """DeepSeek模型工厂类，用于创建不同类型的模型实例"""

    @staticmethod
    def create_chat_model(**kwargs):
        """创建DeepSeek聊天模型"""
        try:
            from crewai import LLM

            config = get_deepseek_model_config()
            model_name = config['chat_model']

            # 合并默认配置和用户配置
            model_config = {
                'model': model_name,
                'base_url': os.getenv('DEEPSEEK_BASE_URL', 'https://api.deepseek.com/v1'),
                'api_key': os.getenv('DEEPSEEK_API_KEY'),
                'max_tokens': config['max_tokens'],
                'temperature': config['temperature'],
                'top_p': config['top_p'],
                **kwargs
            }

            logger.info(f"创建DeepSeek聊天模型: {model_name}")
            return LLM(**model_config)

        except Exception as e:
            logger.error(f"创建DeepSeek聊天模型失败: {str(e)}")
            raise

    @staticmethod
    def create_coder_model(**kwargs):
        """创建DeepSeek代码模型"""
        try:
            from crewai import LLM

            config = get_deepseek_model_config()
            model_name = config['coder_model']

            # 合并默认配置和用户配置
            model_config = {
                'model': model_name,
                'base_url': os.getenv('DEEPSEEK_BASE_URL', 'https://api.deepseek.com/v1'),
                'api_key': os.getenv('DEEPSEEK_API_KEY'),
                'max_tokens': config['max_tokens'],
                'temperature': config['temperature'],
                'top_p': config['top_p'],
                **kwargs
            }

            logger.info(f"创建DeepSeek代码模型: {model_name}")
            return LLM(**model_config)

        except Exception as e:
            logger.error(f"创建DeepSeek代码模型失败: {str(e)}")
            raise