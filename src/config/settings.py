import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 百度ASR/TTS配置
BAIDU_ASR_API_KEY = os.getenv("BAIDU_ASR_API_KEY")
BAIDU_ASR_SECRET_KEY = os.getenv("BAIDU_ASR_SECRET_KEY")

# 千帆配置
QIANFAN_API_KEY = os.getenv("QIANFAN_API_KEY")
QIANFAN_BASE_URL = os.getenv("QIANFAN_BASE_URL", "https://qianfan.baidubce.com/v2")
DEFAULT_CHAT_MODEL = os.getenv("DEFAULT_CHAT_MODEL", "ernie-4.5-turbo-32k")

# 音频配置
TEMP_AUDIO_PATH = os.getenv("TEMP_AUDIO_PATH", "./temp_audio.wav")
AUDIO_RATE = 16000
AUDIO_CHANNELS = 1
AUDIO_CHUNK = 1024
RECORD_DURATION = 5  # 默认录音时长

# UI配置
DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "普通话")
DEFAULT_TTS_ENGINE = os.getenv("DEFAULT_TTS_ENGINE", "offline")
WINDOW_SIZE = "1000x700"
MIN_WINDOW_SIZE = "800x600"
APP_TITLE = "猫猫语音助手（优化版）"

# 验证必要配置
REQUIRED_CONFIGS = [
    ("BAIDU_ASR_API_KEY", BAIDU_ASR_API_KEY),
    ("BAIDU_ASR_SECRET_KEY", BAIDU_ASR_SECRET_KEY),
    ("QIANFAN_API_KEY", QIANFAN_API_KEY)
]
for key_name, key_value in REQUIRED_CONFIGS:
    if not key_value:
        raise ValueError(f"请配置环境变量: {key_name}")