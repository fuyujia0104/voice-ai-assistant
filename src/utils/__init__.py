# src/utils/__init__.py
"""
工具模块：提供音频处理、通用工具函数
"""

# 导出音频工具函数
from .audio_utils import record_audio

__all__ = ["record_audio"]