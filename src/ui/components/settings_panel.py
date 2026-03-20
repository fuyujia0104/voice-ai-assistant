import customtkinter as ctk
from typing import Optional, Callable, Dict, Any
from dataclasses import dataclass


# 定义配置数据结构（规范配置项，避免魔法值）
@dataclass
class AppSettings:
    """应用配置数据类：统一管理所有可配置项"""
    language: str = "普通话"
    enable_search: bool = True  # 默认启用联网搜索，以获取实时信息（如天气）
    tts_engine: str = "offline"
    record_duration: int = 5
    tts_voice: str = "female"
    tts_speed: int = 5


class SettingsPanel(ctk.CTkFrame):
    """
    通用设置面板组件
    封装所有系统配置项（语言、联网搜索、TTS、录音时长等）
    支持配置变更回调、初始值设置、配置导出
    """

    def __init__(
            self,
            parent: ctk.CTkBaseClass,
            initial_settings: Optional[AppSettings] = None,
            on_setting_change: Optional[Callable[[str, Any], None]] = None,
            on_clear_history: Optional[Callable[[], None]] = None,
            **kwargs
    ):
        """
        初始化设置面板
        :param parent: 父容器（如主窗口的侧边栏）
        :param initial_settings: 初始配置（可选，默认使用AppSettings默认值）
        :param on_setting_change: 配置变更回调函数（参数：配置名、新值）
        :param on_clear_history: 清空历史记录回调函数
        :param kwargs: 传递给CTkFrame的额外参数
        """
        super().__init__(parent, corner_radius=10, **kwargs)

        # 初始化配置和回调
        self.settings = initial_settings or AppSettings()
        self.on_setting_change = on_setting_change
        self.on_clear_history = on_clear_history

        # 构建面板UI
        self._create_ui()

    def _create_ui(self):
        """分层构建设置面板UI"""
        # 1. 面板标题
        self._create_title()

        # 2. 语音识别配置组
        self._create_asr_settings()

        # 3. AI对话配置组
        self._create_chat_settings()

        # 4. 语音合成配置组
        self._create_tts_settings()

        # 5. 操作按钮组
        self._create_action_buttons()

    def _create_title(self):
        """创建面板标题"""
        title_label = ctk.CTkLabel(
            self,
            text="⚙️ 系统设置",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=(20, 15))

    def _create_asr_settings(self):
        """创建语音识别配置项"""
        # 配置组容器（视觉分组）
        asr_frame = ctk.CTkFrame(self, fg_color="transparent")
        asr_frame.pack(fill="x", padx=10, pady=5)

        # 组标题
        ctk.CTkLabel(
            asr_frame,
            text="🎙️ 语音识别",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=5, pady=(0, 8))

        # 1. 语言选择
        lang_label = ctk.CTkLabel(asr_frame, text="识别语言：")
        lang_label.pack(anchor="w", padx=10)

        self.lang_var = ctk.StringVar(value=self.settings.language)
        lang_menu = ctk.CTkOptionMenu(
            asr_frame,
            values=["普通话", "英文", "粤语", "重庆话"],
            variable=self.lang_var,
            command=lambda v: self._on_setting_update("language", v)
        )
        lang_menu.pack(fill="x", padx=10, pady=5)

        # 2. 录音时长
        duration_label = ctk.CTkLabel(asr_frame, text="录音时长（秒）：")
        duration_label.pack(anchor="w", padx=10)

        self.duration_var = ctk.IntVar(value=self.settings.record_duration)
        duration_spinbox = ctk.CTkEntry(
            asr_frame,
            textvariable=self.duration_var,
            width=80
        )
        duration_spinbox.pack(anchor="w", padx=10, pady=5)
        # 绑定失去焦点事件（确认输入）
        duration_spinbox.bind(
            "<FocusOut>",
            lambda e: self._on_setting_update("record_duration", self.duration_var.get())
        )

    def _create_chat_settings(self):
        """创建AI对话配置项"""
        chat_frame = ctk.CTkFrame(self, fg_color="transparent")
        chat_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(
            chat_frame,
            text="🤖 AI对话",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=5, pady=(0, 8))

        # 联网搜索开关
        self.search_var = ctk.BooleanVar(value=self.settings.enable_search)
        search_switch = ctk.CTkSwitch(
            chat_frame,
            text="启用实时联网搜索",
            variable=self.search_var,
            command=lambda: self._on_setting_update("enable_search", self.search_var.get())
        )
        search_switch.pack(anchor="w", padx=10, pady=5)

    def _create_tts_settings(self):
        """创建语音合成配置项"""
        tts_frame = ctk.CTkFrame(self, fg_color="transparent")
        tts_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(
            tts_frame,
            text="🔊 语音合成",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=5, pady=(0, 8))

        # TTS引擎选择
        tts_engine_label = ctk.CTkLabel(tts_frame, text="合成引擎：")
        tts_engine_label.pack(anchor="w", padx=10)

        self.tts_engine_var = ctk.StringVar(value=self.settings.tts_engine)
        tts_engine_menu = ctk.CTkOptionMenu(
            tts_frame,
            values=["offline", "online"],
            variable=self.tts_engine_var,
            command=lambda v: self._on_setting_update("tts_engine", v)
        )
        tts_engine_menu.pack(fill="x", padx=10, pady=5)

        # TTS音色选择
        tts_voice_label = ctk.CTkLabel(tts_frame, text="合成音色：")
        tts_voice_label.pack(anchor="w", padx=10)

        self.tts_voice_var = ctk.StringVar(value=self.settings.tts_voice)
        tts_voice_menu = ctk.CTkOptionMenu(
            tts_frame,
            values=["female", "male", "child"],
            variable=self.tts_voice_var,
            command=lambda v: self._on_setting_update("tts_voice", v)
        )
        tts_voice_menu.pack(fill="x", padx=10, pady=5)

        # TTS语速调节
        tts_speed_label = ctk.CTkLabel(tts_frame, text="合成语速（1-10）：")
        tts_speed_label.pack(anchor="w", padx=10)

        self.tts_speed_var = ctk.IntVar(value=self.settings.tts_speed)
        tts_speed_slider = ctk.CTkSlider(
            tts_frame,
            from_=1,
            to=10,
            variable=self.tts_speed_var,
            command=lambda v: self._on_setting_update("tts_speed", int(v))
        )
        tts_speed_slider.pack(fill="x", padx=10, pady=5)

    def _create_action_buttons(self):
        """创建操作按钮（重置、导出配置、清空历史）"""
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=20)

        # 重置配置按钮
        reset_btn = ctk.CTkButton(
            btn_frame,
            text="🔄 重置默认",
            width=100,
            fg_color="#ffc107",
            hover_color="#ffb300",
            command=self.reset_to_default
        )
        reset_btn.pack(side="left", padx=5)

        # 导出配置按钮
        export_btn = ctk.CTkButton(
            btn_frame,
            text="📤 导出配置",
            width=100,
            fg_color="#17a2b8",
            hover_color="#138496",
            command=self.export_settings
        )
        export_btn.pack(side="right", padx=5)

        # 清空历史记录按钮
        if self.on_clear_history:
            clear_history_btn = ctk.CTkButton(
                btn_frame,
                text="🗑️ 清空历史",
                width=100,
                fg_color="#dc3545",
                hover_color="#c82333",
                command=self.on_clear_history
            )
            clear_history_btn.pack(side="bottom", pady=10)

    def _on_setting_update(self, setting_name: str, value: Any):
        """
        配置更新统一处理
        :param setting_name: 配置项名称
        :param value: 新值
        """
        # 更新本地配置
        setattr(self.settings, setting_name, value)
        # 触发外部回调（通知主窗口配置变更）
        if self.on_setting_change:
            self.on_setting_change(setting_name, value)

    def get_current_settings(self) -> AppSettings:
        """获取当前配置（返回数据类实例）"""
        return self.settings

    def reset_to_default(self):
        """重置为默认配置"""
        default = AppSettings()
        self.lang_var.set(default.language)
        self.search_var.set(default.enable_search)
        self.tts_engine_var.set(default.tts_engine)
        self.duration_var.set(default.record_duration)
        self.tts_voice_var.set(default.tts_voice)
        self.tts_speed_var.set(default.tts_speed)
        # 同步更新本地配置并触发回调
        for key in AppSettings.__annotations__.keys():
            self._on_setting_update(key, getattr(default, key))

    def export_settings(self) -> Dict[str, Any]:
        """导出配置为字典（可保存到文件）"""
        settings_dict = {
            "language": self.settings.language,
            "enable_search": self.settings.enable_search,
            "tts_engine": self.settings.tts_engine,
            "record_duration": self.settings.record_duration,
            "tts_voice": self.settings.tts_voice,
            "tts_speed": self.settings.tts_speed
        }
        # 可选：保存到json文件
        # import json
        # with open("app_settings.json", "w", encoding="utf-8") as f:
        #     json.dump(settings_dict, f, ensure_ascii=False, indent=4)
        return settings_dict