import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# Hugging Face镜像源配置
HF_ENDPOINT = os.getenv("HF_ENDPOINT", "https://hf-mirror.com")

# 百度ASR/TTS配置
BAIDU_ASR_API_KEY = os.getenv("BAIDU_ASR_API_KEY")
BAIDU_ASR_SECRET_KEY = os.getenv("BAIDU_ASR_SECRET_KEY")

# Qwen配置
# 如果有本地模型，设置为本地路径；否则使用Hugging Face模型ID
QWEN_MODEL_PATH = os.getenv("QWEN_MODEL_PATH", "Qwen/Qwen-1_8B-Chat")
QWEN_DEVICE = os.getenv("QWEN_DEVICE", "auto")  # auto/cuda/cpu
DEFAULT_CHAT_ENGINE = os.getenv("DEFAULT_CHAT_ENGINE", "api")  # api(千帆API)/local(Qwen)

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
WINDOW_SIZE = "1200x800"
MIN_WINDOW_SIZE = "900x700"
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
