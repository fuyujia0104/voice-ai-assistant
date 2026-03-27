from src.core.chat import QianFanChat
from src.core.qwen_chat import QwenChat
from src.config.settings import DEFAULT_CHAT_ENGINE, QWEN_MODEL_PATH, QWEN_DEVICE


class ChatManager:
    """对话管理器,支持API和本地模型双方案"""

    def __init__(self):
        self.engine = DEFAULT_CHAT_ENGINE
        self.api_chat = QianFanChat()
        self.local_chat = None  # 延迟加载本地模型

        # 如果默认引擎是本地模型,立即加载
        if self.engine == "local":
            self._load_local_model()

    def _load_local_model(self):
        """加载本地Qwen模型"""
        if self.local_chat is None:
            self.local_chat = QwenChat(
                model_path=QWEN_MODEL_PATH,
                device=QWEN_DEVICE
            )

    def switch_engine(self, engine):
        """切换对话引擎"""
        if engine not in ["api", "local"]:
            raise ValueError("引擎必须是'api'或'local'")

        self.engine = engine
        if engine == "local":
            self._load_local_model()

    def send_message(self, user_input, enable_search=False):
        """发送消息,根据当前引擎选择实现"""
        try:
            if self.engine == "api":
                return self.api_chat.send_message(user_input, enable_search)
            else:
                # 确保本地模型已加载
                if self.local_chat is None:
                    self._load_local_model()
                return self.local_chat.send_message(user_input, enable_search)
        except Exception as e:
            print(f"ChatManager.send_message错误: {str(e)}")
            import traceback
            traceback.print_exc()
            # 如果本地模型失败，尝试切换到API模式
            if self.engine == "local":
                print("本地模型失败，尝试切换到API模式...")
                self.engine = "api"
                return self.api_chat.send_message(user_input, enable_search)
            else:
                raise

    def clear_history(self):
        """清空对话历史"""
        self.api_chat.clear_history()
        if self.local_chat:
            self.local_chat.clear_history()
