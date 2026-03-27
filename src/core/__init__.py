# src/core/__init__.py
"""
核心业务模块：实现语音识别、合成、AI对话的核心逻辑
"""

# 导出核心类
from .asr import BaiduASR
from .tts import TTS
from .chat import QianFanChat
from .qwen_chat import ChatGLMChat
from .chat_manager import ChatManager

__all__ = ["BaiduASR", "TTS", "QianFanChat", "ChatGLMChat", "ChatManager"]
