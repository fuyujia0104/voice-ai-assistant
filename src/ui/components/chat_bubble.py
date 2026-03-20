# src/ui/components/chat_bubble.py
import customtkinter as ctk
from datetime import datetime
from typing import Optional, Literal


class ChatBubble(ctk.CTkFrame):
    """
    通用聊天气泡组件
    支持用户/AI 消息区分、时间戳、自定义样式、自动换行
    """

    def __init__(
            self,
            parent: ctk.CTkBaseClass,
            sender: str,
            message: str,
            role: Literal["user", "assistant"] = "user",
            timestamp: Optional[str] = None,
            **kwargs
    ):
        """
        初始化聊天气泡
        :param parent: 父容器（如 CTkScrollableFrame）
        :param sender: 发送者名称（如 "我"、"猫猫AI"）
        :param message: 消息内容
        :param role: 角色（user/assistant），决定气泡样式
        :param timestamp: 时间戳（默认自动生成当前时间）
        :param kwargs: 传递给 CTkFrame 的额外参数（如 width、height）
        """
        # 基础样式配置（按角色区分）
        if role == "user":
            fg_color = "#007bff"  # 蓝色（用户）
            text_color = "white"
            time_color = "#cccccc"  # 浅灰色
            anchor = "e"  # 右对齐
        else:
            fg_color = "#f8f9fa"  # 浅灰色（AI）
            text_color = "#212529"  # 深灰色
            time_color = "#6c757d"  # 灰色
            anchor = "w"  # 左对齐

        # 初始化父类
        super().__init__(parent, fg_color=fg_color, corner_radius=15, **kwargs)

        # 自动生成时间戳（格式：HH:MM:SS）
        self.timestamp = timestamp or datetime.now().strftime("%H:%M:%S")

        # 1. 时间戳标签（小号字体，半透明）
        self.time_label = ctk.CTkLabel(
            self,
            text=self.timestamp,
            font=ctk.CTkFont(size=10, weight="normal"),
            text_color=time_color
        )
        self.time_label.pack(anchor=anchor, padx=10, pady=(5, 0))

        # 2. 发送者标签（加粗）
        self.sender_label = ctk.CTkLabel(
            self,
            text=sender,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=text_color
        )
        self.sender_label.pack(anchor=anchor, padx=10, pady=(0, 3))

        # 3. 消息内容标签（自动换行，最大宽度限制）
        self.message_label = ctk.CTkLabel(
            self,
            text=message,
            font=ctk.CTkFont(size=14),
            text_color=text_color,
            wraplength=600,  # 最大宽度，超出自动换行
            justify="left"
        )
        self.message_label.pack(anchor=anchor, padx=10, pady=(0, 5))

    @staticmethod
    def create_bubble(
            parent: ctk.CTkBaseClass,
            sender: str,
            message: str,
            role: Literal["user", "assistant"] = "user",
            timestamp: Optional[str] = None
    ) -> "ChatBubble":
        """
        静态工厂方法：快速创建聊天气泡并添加到父容器
        :return: 创建好的 ChatBubble 实例
        """
        bubble = ChatBubble(parent, sender, message, role, timestamp)
        # 气泡布局：按角色对齐，添加间距
        bubble.pack(
            anchor="e" if role == "user" else "w",
            padx=20,
            pady=5,
            fill="x",
            ipady=8,  # 内部垂直间距
            ipadx=10  # 内部水平间距
        )
        return bubble