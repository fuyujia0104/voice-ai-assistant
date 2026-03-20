from tkinter import messagebox
from src.ui.main_window import VoiceAssistantApp

if __name__ == "__main__":
    try:
        app = VoiceAssistantApp()
        app.mainloop()
    except Exception as e:
        import traceback
        traceback.print_exc()
        messagebox.showerror("启动失败", f"应用启动失败：{str(e)}\n\n详情请查看控制台输出。")