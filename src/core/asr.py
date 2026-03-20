import base64
import requests
from src.config import BAIDU_ASR_API_KEY, BAIDU_ASR_SECRET_KEY

class BaiduASR:
    def __init__(self):
        self.token = self._get_token()
        self.url = "https://vop.baidu.com/server_api"
        self.lang_map = {
            "普通话": "1537",
            "英文": "1737",
            "粤语": "1637",
            "重庆话": "1837"
        }

    def _get_token(self):
        auth_url = f"https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id={BAIDU_ASR_API_KEY}&client_secret={BAIDU_ASR_SECRET_KEY}"
        resp = requests.post(auth_url)
        if resp.status_code == 200:
            return resp.json().get('access_token')
        else:
            raise Exception(f"获取百度ASR token失败: {resp.text}")

    def recognize(self, audio_path, language="普通话"):
        with open(audio_path, 'rb') as f:
            audio_data = f.read()
        speech = base64.b64encode(audio_data).decode('utf-8')
        payload = {
            'format': 'wav',
            'rate': 16000,
            'channel': 1,
            'cuid': 'python_assistant',
            'token': self.token,
            'speech': speech,
            'len': len(audio_data),
            'dev_pid': self.lang_map.get(language, "1537")
        }
        headers = {'Content-Type': 'application/json'}
        resp = requests.post(self.url, json=payload, headers=headers)
        result = resp.json()
        if result.get('err_no') == 0:
            return result.get('result')[0]  # 返回识别文本
        else:
            raise Exception(f"ASR错误: {result.get('err_msg')}")