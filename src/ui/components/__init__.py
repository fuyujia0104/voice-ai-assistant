# src/ui/components/__init__.py
"""
UI组件模块：提供聊天气泡、设置面板等通用UI组件
"""

from .chat_bubble import ChatBubble
from .settings_panel import SettingsPanel, AppSettings
__all__ = ["ChatBubble", "SettingsPanel", "AppSettings"]
