import pyttsx3
import requests
import base64
import pygame
import tempfile
import os
import threading
from src.config import BAIDU_ASR_API_KEY, BAIDU_ASR_SECRET_KEY

class TTS:
    def __init__(self, engine="offline"):
        self.engine = engine
        self.speak_lock = threading.Lock()  # 添加线程锁
        if engine == "offline":
            self._init_offline()
        elif engine == "online":
            self._init_online()

    def _init_offline(self):
        self.offline_engine = pyttsx3.init()
        # 可设置语速、音量等
        self.offline_engine.setProperty('rate', 150)
        self.offline_engine.setProperty('volume', 0.9)

    def _init_online(self):
        self.token = self._get_online_token()
        self.url = "https://tsn.baidu.com/text2audio"

    def _get_online_token(self):
        auth_url = f"https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id={BAIDU_ASR_API_KEY}&client_secret={BAIDU_ASR_SECRET_KEY}"
        resp = requests.post(auth_url)
        if resp.status_code == 200:
            return resp.json().get('access_token')
        else:
            raise Exception(f"获取百度TTS token失败: {resp.text}")

    def speak(self, text):
        if self.engine == "offline":
            # 使用线程锁防止并发调用runAndWait()
            with self.speak_lock:
                self.offline_engine.say(text)
                self.offline_engine.runAndWait()
        else:
            # 在线TTS，返回音频并播放
            params = {
                'tex': text,
                'tok': self.token,
                'cuid': 'python_assistant',
                'ctp': 1,
                'lan': 'zh',
                'spd': 5,
                'pit': 5,
                'vol': 9,
                'per': 0  # 0为女声，1为男声
            }
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            resp = requests.post(self.url, data=params, headers=headers)
            if resp.headers.get('Content-Type') == 'audio/wav':
                # 保存临时文件并播放
                with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as f:
                    f.write(resp.content)
                    temp_path = f.name
                pygame.mixer.init()
                pygame.mixer.music.load(temp_path)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    continue
                os.unlink(temp_path)
            else:
                raise Exception(f"TTS错误: {resp.text}")

    def set_voice(self, voice_type):
        """设置合成音色"""
        if self.engine == "offline":
            voices = self.offline_engine.getProperty('voices')
            if voice_type == "male":
                # 选择男声（需系统有对应语音包）
                self.offline_engine.setProperty('voice', voices[0].id if voices else None)
            elif voice_type == "female":
                self.offline_engine.setProperty('voice', voices[1].id if len(voices)>=2 else None)
            elif voice_type == "child":
                # 部分系统有童声，需适配
                self.offline_engine.setProperty('voice', voices[2].id if len(voices)>=3 else None)

    def set_speed(self, speed):
        """设置合成语速（1-10映射为实际速度值）"""
        if self.engine == "offline":
            # 离线引擎速度范围通常是 0-200，映射1-10到80-200
            self.offline_engine.setProperty('rate', 80 + (speed-1)*12)
        else:
            # 在线引擎 speed 参数是1-10，直接保存，在speak时使用
            self.online_speed = speed