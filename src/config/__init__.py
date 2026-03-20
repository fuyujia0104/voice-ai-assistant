# src/config/__init__.py
"""
配置模块：统一管理项目环境变量、常量配置
"""

# 导出 settings 中的核心配置（简化导入）
from .settings import (
    BAIDU_ASR_API_KEY,
    BAIDU_ASR_SECRET_KEY,
    QIANFAN_API_KEY,
    DEFAULT_CHAT_MODEL,
    TEMP_AUDIO_PATH,
    WINDOW_SIZE
)

__all__ = [
    "BAIDU_ASR_API_KEY",
    "BAIDU_ASR_SECRET_KEY",
    "QIANFAN_API_KEY",
    "DEFAULT_CHAT_MODEL",
    "TEMP_AUDIO_PATH",
    "WINDOW_SIZE"
]