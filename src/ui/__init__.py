# src/ui/__init__.py
"""
UI模块：实现应用的界面布局和交互逻辑
"""

# 导出主窗口类（外部仅需导入这个即可启动UI）
from .main_window import VoiceAssistantApp

__all__ = ["VoiceAssistantApp"]