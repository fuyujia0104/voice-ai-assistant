# src/__init__.py
"""
猫猫语音助手核心包
包含语音识别、合成、AI对话等核心功能
"""

# 对外暴露核心类/模块（简化导入）
from .core.asr import BaiduASR
from .core.tts import TTS
from .core.chat import QianFanChat

# 限定 import * 时导出的内容（规范接口）
__all__ = ["BaiduASR", "TTS", "QianFanChat"]

# 包版本
__version__ = "1.0.0"