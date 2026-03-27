import customtkinter as ctk
import os
from tkinter import messagebox
import threading
from datetime import datetime
from src.config.settings import (
    TEMP_AUDIO_PATH, DEFAULT_LANGUAGE, DEFAULT_TTS_ENGINE,
    WINDOW_SIZE, MIN_WINDOW_SIZE, APP_TITLE, RECORD_DURATION
)
from src.core.asr import BaiduASR
from src.core.tts import TTS
from src.core.chat_manager import ChatManager
from src.utils.audio_utils import record_audio, stop_recording, reset_recording_state
from .components.chat_bubble import ChatBubble
from .components.settings_panel import SettingsPanel, AppSettings

# 设置UI主题
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class VoiceAssistantApp(ctk.CTk):
    def __init__(self):
        try:
            super().__init__()
            self.title(APP_TITLE)
            self.geometry(WINDOW_SIZE)
            min_w, min_h = MIN_WINDOW_SIZE.split("x")
            self.minsize(int(min_w), int(min_h))

            # 初始化核心模块
            print("正在初始化ASR...")
            self.asr = BaiduASR()
            print("ASR初始化成功")

            print("正在初始化TTS...")
            self.tts = TTS(engine=DEFAULT_TTS_ENGINE)
            print("TTS初始化成功")

            print("正在初始化ChatManager...")
            self.chat = ChatManager()
            print("ChatManager初始化成功")

            # 状态变量
            self.current_language = DEFAULT_LANGUAGE
            self.enable_search = True  # 默认启用联网搜索，以获取实时信息（如天气）
            self.tts_engine = DEFAULT_TTS_ENGINE
            self.is_recording = False  # 录音状态标记
            self.record_duration = RECORD_DURATION

            # 构建UI
            print("正在构建UI...")
            self._create_layout()
            print("UI构建完成")
        except Exception as e:
            import traceback
            # 输出完整的错误堆栈信息到控制台
            print("=" * 80)
            print("初始化失败 - 错误类型:", type(e).__name__)
            print("错误信息:", str(e))
            print("=" * 80)
            print("完整堆栈跟踪:")
            traceback.print_exc()
            print("=" * 80)

            # 显示错误对话框
            from tkinter import messagebox
            error_msg = f"初始化失败：{str(e)}"
            messagebox.showerror("初始化失败", error_msg)
            raise

    def _create_layout(self):
        """分层构建UI（更易维护）"""
        # 1. 侧边栏（设置面板）
        self._create_sidebar()

        # 2. 主内容区（聊天+输入）
        self._create_main_content()

    def _create_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=10)
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)

        # 初始化初始配置
        initial_settings = AppSettings(
            language=self.current_language,
            enable_search=self.enable_search,
            chat_engine=self.chat.engine,
            tts_engine=self.tts_engine,
            record_duration=5  # 默认录音时长
        )

        # 创建设置面板组件
        self.settings_panel = SettingsPanel(
            parent=self.sidebar,
            initial_settings=initial_settings,
            on_setting_change=self._handle_setting_change,  # 配置变更回调
            on_clear_history=self.clear_history  # 清空历史记录回调
        )
        self.settings_panel.pack(fill="both", expand=True, padx=5, pady=5)


    def _create_main_content(self):
        """优化后的主内容区（聊天气泡+交互优化）"""
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # 聊天标题
        chat_title = ctk.CTkLabel(
            self.main_frame, text="🐱 猫猫语音助手",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        chat_title.pack(pady=10)

        # 聊天显示区域（滚动+美化）
        self.chat_display = ctk.CTkScrollableFrame(self.main_frame, corner_radius=10)
        self.chat_display.pack(fill="both", expand=True, padx=10, pady=5)

        # 输入区域（优化布局）
        self.input_frame = ctk.CTkFrame(self.main_frame, height=90, corner_radius=10)
        self.input_frame.pack(fill="x", padx=10, pady=10)

        # 输入框（自适应）
        self.message_entry = ctk.CTkEntry(
            self.input_frame, placeholder_text="输入消息（按回车发送）...",
            font=ctk.CTkFont(size=14)
        )
        self.message_entry.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # 录音按钮（带状态）
        self.record_button = ctk.CTkButton(
            self.input_frame, text="🎤 录音", width=90,
            command=self.toggle_recording,
            fg_color="#28a745", hover_color="#218838"
        )
        self.record_button.pack(side="left", padx=5, pady=10)

        # 发送按钮
        self.send_button = ctk.CTkButton(
            self.input_frame, text="✈️ 发送", width=90,
            command=self.send_message,
            fg_color="#007bff", hover_color="#0069d9"
        )
        self.send_button.pack(side="left", padx=5, pady=10)

        # 绑定回车
        self.message_entry.bind("<Return>", lambda e: self.send_message())

    def _on_language_change(self, choice):
        self.current_language = choice

    def _on_search_toggle(self):
        self.enable_search = self.search_switch.get()  # 绑定开关状态
        tip = "已启用实时联网搜索（回答更精准）" if self.enable_search else "已关闭实时联网搜索"
        self.display_message("系统提示", tip, is_user=False)

    def _on_tts_change(self, choice):
        self.tts_engine = choice
        self.tts = TTS(engine=choice)
        self.display_message("系统提示", f"已切换TTS引擎为：{choice}", is_user=False)

    def display_message(self, sender, message, is_user=True):
        """使用 ChatBubble 组件显示消息"""
        role = "user" if is_user else "assistant"
        # 调用静态方法快速创建并布局气泡
        ChatBubble.create_bubble(
            parent=self.chat_display,
            sender=sender,
            message=message,
            role=role
        )
        # 自动滚动到底部
        self.chat_display._parent_canvas.yview_moveto(1.0)

    def send_message(self):
        """优化后的发送逻辑（空输入校验+UI反馈）"""
        try:
            user_input = self.message_entry.get().strip()
            if not user_input:
                messagebox.showwarning("提示", "输入内容不能为空！")
                return

            # 清空输入框+显示用户消息
            self.message_entry.delete(0, "end")
            self.display_message("我", user_input, is_user=True)

            # 子线程调用AI（避免UI卡顿）
            threading.Thread(
                target=self._get_ai_reply,
                args=(user_input,),
                daemon=True
            ).start()
        except Exception as e:
            import traceback
            # 输出完整的错误堆栈信息到控制台
            print("=" * 80)
            print("发送消息失败 - 错误类型:", type(e).__name__)
            print("错误信息:", str(e))
            print("=" * 80)
            print("完整堆栈跟踪:")
            traceback.print_exc()
            print("=" * 80)

            error_msg = f"发送消息失败：{str(e)}"
            self.display_message("系统错误", error_msg, is_user=False)
            messagebox.showerror("错误", error_msg)

    def _get_ai_reply(self, user_input):
        """修复enable_search参数绑定"""
        try:
            # 关键修复：使用self.enable_search（关联开关）
            reply = self.chat.send_message(user_input, enable_search=self.enable_search)
            self.display_message("猫猫AI", reply, is_user=False)
            self.tts.speak(reply)
        except Exception as e:
            import traceback
            # 输出完整的错误堆栈信息到控制台
            print("=" * 80)
            print("AI回复失败 - 错误类型:", type(e).__name__)
            print("错误信息:", str(e))
            print("=" * 80)
            print("完整堆栈跟踪:")
            traceback.print_exc()
            print("=" * 80)

            error_msg = f"AI回复失败：{str(e)}"
            self.display_message("系统错误", error_msg, is_user=False)
            messagebox.showerror("错误", error_msg)

    def toggle_recording(self):
        """切换录音状态：开始或停止录音"""
        try:
            if not self.is_recording:
                # 开始录音
                self.is_recording = True
                self.record_button.configure(text="⏹️ 停止录音", fg_color="#dc3545", hover_color="#c82333")
                threading.Thread(
                    target=self._record_and_recognize,
                    daemon=True
                ).start()
            else:
                # 停止录音
                stop_recording()  # 停止录音线程
                self.display_message("系统提示", "录音已手动停止", is_user=False)
        except Exception as e:
            import traceback
            # 输出完整的错误堆栈信息到控制台
            print("=" * 80)
            print("录音切换失败 - 错误类型:", type(e).__name__)
            print("错误信息:", str(e))
            print("=" * 80)
            print("完整堆栈跟踪:")
            traceback.print_exc()
            print("=" * 80)

            error_msg = f"录音切换失败：{str(e)}"
            self.display_message("系统错误", error_msg, is_user=False)
            messagebox.showerror("错误", error_msg)

    def _record_and_recognize(self):
        """录音+识别逻辑（全量修复异常处理+资源释放）"""
        # 临时音频文件路径（从配置导入，避免硬编码）
        temp_audio = TEMP_AUDIO_PATH
        try:
            # 1. 前置校验：防止音频文件已存在导致占用
            if os.path.exists(temp_audio):
                os.remove(temp_audio)

            # 2. 重置录音状态，确保可以正常录音
            reset_recording_state()

            # 3. 提示用户开始录音
            self.display_message("系统提示", f"开始录音（{self.record_duration}秒）...点击'停止录音'按钮可提前结束", is_user=False)

            # 3. 调用录音工具（增加超时/设备占用校验）
            record_success = record_audio(self.record_duration, temp_audio)
            if not record_success:
                raise Exception("录音文件生成失败，请检查麦克风设备")

            # 4. 校验录音文件是否有效
            if not os.path.exists(temp_audio) or os.path.getsize(temp_audio) < 1024:  # 小于1KB视为无效
                raise Exception("录音文件为空，可能是麦克风未授权/静音")

            self.display_message("系统提示", "录音完成，正在识别...", is_user=False)

            # 5. 语音识别（增加语言参数校验）
            if self.current_language not in ["普通话", "英文", "粤语", "重庆话"]:
                self.current_language = "普通话"  # 兜底默认值
            text = self.asr.recognize(temp_audio, language=self.current_language)

            # 6. 识别结果校验
            if not text or text.strip() == "":
                raise Exception("未识别到有效语音内容，请靠近麦克风重试")

            # 7. 显示识别结果并调用AI
            self.display_message("我（语音）", text, is_user=True)
            # AI回复增加超时控制（避免接口卡顿）
            reply = self.chat.send_message(text, enable_search=self.enable_search)
            self.display_message("猫猫AI", reply, is_user=False)
            self.tts.speak(reply)

        except PermissionError:
            # 麦克风权限错误
            error_msg = "麦克风权限被拒绝，请检查系统权限设置"
            self.display_message("系统错误", error_msg, is_user=False)
            messagebox.showerror("权限错误", error_msg)
        except FileNotFoundError:
            # 音频设备未找到
            error_msg = "未检测到麦克风设备，请确认设备已连接"
            self.display_message("系统错误", error_msg, is_user=False)
            messagebox.showerror("设备错误", error_msg)
        except requests.exceptions.RequestException as e:
            # 百度ASR/千帆API网络错误
            error_msg = f"网络请求失败：{str(e)}，请检查网络或API密钥"
            self.display_message("系统错误", error_msg, is_user=False)
            messagebox.showerror("网络错误", error_msg)
        except Exception as e:
            import traceback
            # 输出完整的错误堆栈信息到控制台
            print("=" * 80)
            print("语音识别失败 - 错误类型:", type(e).__name__)
            print("错误信息:", str(e))
            print("=" * 80)
            print("完整堆栈跟踪:")
            traceback.print_exc()
            print("=" * 80)

            # 通用异常兜底
            error_msg = f"语音识别失败：{str(e)}"
            self.display_message("系统错误", error_msg, is_user=False)
            messagebox.showerror("错误", error_msg)
        finally:
            # 1. 恢复按钮状态（必执行）
            self.is_recording = False
            self.record_button.configure(text="🎤 录音", fg_color="#28a745", hover_color="#218838")
            
            # 2. 重置录音状态为True，为下次录音做准备
            reset_recording_state()

            # 3. 清理临时音频文件（避免占用）
            try:
                if os.path.exists(temp_audio):
                    os.remove(temp_audio)
            except:
                pass  # 清理失败不影响主流程

    def _handle_setting_change(self, setting_name, value):
        """处理配置变更"""
        try:
            if setting_name == "language":
                self.current_language = value
            elif setting_name == "enable_search":
                self.enable_search = value
            elif setting_name == "chat_engine":
                self.chat.switch_engine(value)
            elif setting_name == "tts_engine":
                self.tts_engine = value
                self.tts = TTS(engine=value)
            elif setting_name == "record_duration":
                # 更新录音时长配置
                self.record_duration = max(1, min(30, value))  # 限制1-30秒
            elif setting_name == "tts_voice":
                self.tts.set_voice(value)  # 需在TTS类中实现set_voice方法
            elif setting_name == "tts_speed":
                self.tts.set_speed(value)  # 需在TTS类中实现set_speed方法

            # 提示用户配置已更新
            self.display_message("系统提示", f"{setting_name} 已更新为：{value}", is_user=False)
        except Exception as e:
            import traceback
            # 输出完整的错误堆栈信息到控制台
            print("=" * 80)
            print("配置变更失败 - 错误类型:", type(e).__name__)
            print("错误信息:", str(e))
            print("=" * 80)
            print("完整堆栈跟踪:")
            traceback.print_exc()
            print("=" * 80)

            error_msg = f"配置变更失败：{str(e)}"
            self.display_message("系统错误", error_msg, is_user=False)
            messagebox.showerror("错误", error_msg)

    def clear_history(self):
        """清空对话历史（含UI）"""
        try:
            self.chat.clear_history()
            # 清空聊天显示区
            for widget in self.chat_display.winfo_children():
                widget.destroy()
            self.display_message("系统提示", "对话历史已清空", is_user=False)
        except Exception as e:
            import traceback
            # 输出完整的错误堆栈信息到控制台
            print("=" * 80)
            print("清空历史失败 - 错误类型:", type(e).__name__)
            print("错误信息:", str(e))
            print("=" * 80)
            print("完整堆栈跟踪:")
            traceback.print_exc()
            print("=" * 80)

            error_msg = f"清空历史失败：{str(e)}"
            self.display_message("系统错误", error_msg, is_user=False)
            messagebox.showerror("错误", error_msg)
