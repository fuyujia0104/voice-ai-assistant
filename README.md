# voice-ai-assistant 

一个基于百度千帆大模型、百度语音识别（ASR）/语音合成（TTS）API 开发的轻量级语音交互 AI 助手，支持实时语音提问、智能回答、语音合成输出，可查询实时天气、资讯等联网信息，内置可视化操作界面。

## 🌟 核心功能
- **实时语音识别**：基于百度 ASR 实现高准确率的中文语音转文字，支持麦克风实时输入
- **智能对话交互**：集成百度千帆大模型（ERNIE 3.5/4.0），支持联网搜索获取实时数据
- **多模式语音合成**：支持百度在线 TTS（高音质）和离线 TTS（无网络可用），可自定义语速/音色
- **可视化操作界面**：基于 Pygame 开发的简洁交互界面，支持一键录音、停止、清空对话
- **实时联网查询**：天气、新闻等实时信息查询，告别静态训练数据

## 📋 环境要求
- Python 3.9 及以上版本（推荐 3.10/3.12）
- 操作系统：Windows（优先）/Linux/macOS
- 网络环境：需联网调用百度 API（离线 TTS 除外）
- 硬件：麦克风、扬声器（语音交互必备）

## 🚀 快速开始

### 1. 克隆仓库
```bash
git clone https://github.com/fuyujia0104/voice-ai-assistant.git
cd voice-ai-assistant
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置 API 密钥
创建一个`.env`文件
示例如下：
`.env`
# 百度语音识别/合成 API
BAIDU_ASR_API_KEY=YOUR_BAIDU_ASR_API_KEY
BAIDU_ASR_SECRET_KEY=YOUR_BAIDU_ASR_SECRET_KEY
# 百度千帆平台 API Key
QIANFAN_API_KEY=YOUR_QIANFAN_API_KEY
# 临时音频文件路径
TEMP_AUDIO_PATH=./temp_audio.wav

# 默认语言和TTS引擎
DEFAULT_LANGUAGE=普通话
DEFAULT_TTS_ENGINE=offline
DEFAULT_CHAT_MODEL=YOUR_DEFAULT_CHAT_MODEL

在 `.env` 文件中填写你的百度 API 密钥，包括 ASR、TTS 和千帆大模型的密钥。

### 4. 运行程序
```bash
python main.py
```

### 5. 开始语音交互
- 点击界面上的“录音”按钮开始录音
- 录音结束后，点击“停止”按钮

### 6.常见问题
Q1: 运行报错 401 Unauthorized
原因：API Key 错误 / 过期、权限未开通、请求头格式错误
解决：
1.核对 .env 中 API Key 与百度控制台完全一致（无多余空格 / 符号）
2.确认千帆模型、语音识别 / 合成服务已在控制台「开通并生效」

Q2: 天气查询返回旧数据（如 2024 年）
原因：联网搜索功能未启用、模型不支持联网
解决：
1.确保 src/core/chat.py 中启用 enable_plugin: true
2.将 DEFAULT_CHAT_MODEL 改为 ernie-3.5-turbo/ernie-4.0-turbo（支持联网）
3.系统提示词中强制要求「基于实时数据回答」

Q3: 语音合成无声音 / 卡顿
原因：Pygame 音频初始化失败、TTS 参数错误、音频设备占用
解决：
1.重启项目并确保无其他程序占用麦克风 / 扬声器
2.检查 src/core/tts.py 中语速（spd）、音量（vol）参数在合理范围（1-15）
3.切换离线 TTS 引擎测试

Q4: Pygame 报 comtypes 警告
原因：资源释放不彻底（非致命错误）
解决：优化 TTS 模块中 Pygame 音频资源的创建 / 销毁逻辑

### 7.🛠️ 技术栈
语音处理：百度 ASR/TTS API、PyAudio（麦克风采集）
AI 对话：百度千帆大模型 SDK、Requests（API 调用）
界面开发：Pygame（可视化交互）
配置管理：python-dotenv（环境变量）
