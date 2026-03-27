from tkinter import messagebox
from src.ui.main_window import VoiceAssistantApp
import sys
import traceback

if __name__ == "__main__":
    try:
        app = VoiceAssistantApp()
        app.mainloop()
    except Exception as e:
        # 输出完整的错误堆栈信息
        print("=" * 80)
        print("错误类型:", type(e).__name__)
        print("错误信息:", str(e))
        print("=" * 80)
        print("完整堆栈跟踪:")
        traceback.print_exc()
        print("=" * 80)

        # 显示错误对话框
        error_msg = f"应用启动失败：{str(e)}\n\n错误类型: {type(e).__name__}\n\n详情请查看控制台输出。"
        messagebox.showerror("启动失败", error_msg)
        sys.exit(1)
