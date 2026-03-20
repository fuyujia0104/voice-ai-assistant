import requests
import json
from datetime import datetime
from src.config.settings import QIANFAN_API_KEY, QIANFAN_BASE_URL, DEFAULT_CHAT_MODEL

class QianFanChat:
    """使用 requests 直接调用千帆 API"""

    def __init__(self, system_prompt="你是猫猫AI，一个友好、可爱的助手。当用户询问实时信息（如天气、日期、新闻等）时，你必须使用联网搜索功能获取准确信息。不要编造或猜测答案。"):
        self.api_key = QIANFAN_API_KEY
        self.base_url = QIANFAN_BASE_URL  
        self.model = DEFAULT_CHAT_MODEL   
        self.system_prompt = system_prompt
        self.messages = [{"role": "system", "content": system_prompt}]

    def send_message(self, user_input, enable_search=False):
        """
        发送消息并获取 AI 回复
        :param user_input: 用户输入
        :param enable_search: 是否启用联网搜索（此处暂不处理，由模型自身决定）
        """
        # 将用户消息加入历史
        self.messages.append({"role": "user", "content": user_input})

        # 构造请求体（完全匹配官方文档）
        # 在每次请求时，将当前日期作为系统消息的一部分发送给AI
        current_date = datetime.now().strftime("%Y年%m月%d日")
        messages_with_date = [
            {"role": "system", "content": f"{self.system_prompt} 当前日期是：{current_date}。"},
            *self.messages[1:]  # 排除原来的system消息
        ]
        payload = {
            "model": self.model,
            "messages": messages_with_date,
            "temperature": 0.7,
            "top_p": 0.95
        }
        # 启用联网搜索以获取实时信息（如天气）
        if enable_search:
            # ernie-4.0-turbo模型支持通过tools参数启用联网搜索
            payload["tools"] = [{
                "type": "web_search",
                "web_search": {
                    "enable": True,
                    "search_result": True
                }
            }]

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }

        try:
            # 使用完整的API端点URL
            url = "https://qianfan.baidubce.com/v2/chat/completions"
            
            # 打印请求信息用于调试
            print(f"请求URL: {url}")
            print(f"请求头: {headers}")
            print(f"请求体: {json.dumps(payload, ensure_ascii=False, indent=2)}")
            
            response = requests.post(
                url,
                headers=headers,
                data=json.dumps(payload, ensure_ascii=False).encode('utf-8')
            )
            
            # 打印响应信息用于调试
            print(f"响应状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
            
            response.raise_for_status()  # 抛出 HTTP 错误
            result = response.json()

            # 解析回复
            reply = result['choices'][0]['message']['content']
            self.messages.append({"role": "assistant", "content": reply})
            return reply
        except requests.exceptions.RequestException as e:
            raise Exception(f"AI回复失败（网络错误）: {str(e)}")
        except (KeyError, json.JSONDecodeError) as e:
            raise Exception(f"AI回复解析失败: {str(e)}，原始响应：{response.text}")

    def clear_history(self):
        """清空对话历史"""
        self.messages = [{"role": "system", "content": self.system_prompt}]