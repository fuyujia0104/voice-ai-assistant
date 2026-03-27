
import torch
import os
from transformers import AutoTokenizer, AutoModelForCausalLM
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

class QwenChat:
    def __init__(self, model_path="", device="auto"):
        # 从环境变量读取模型路径，如果没有提供则使用传入的参数
        self.model_path = model_path or os.getenv("QWEN_MODEL_PATH")
        if not self.model_path:
            raise ValueError("请设置环境变量 QWEN_MODEL_PATH 或传入 model_path 参数")
        
        # 从环境变量读取设备类型，如果没有提供则使用传入的参数
        self.device = device or os.getenv("QWEN_DEVICE", "cpu")

        print("✅ 加载 Windows CPU 专用模型 Qwen-1.8B")


        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_path,
            trust_remote_code=True,
            local_files_only=True
        )

        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_path,
            trust_remote_code=True,
            local_files_only=True,
            torch_dtype=torch.float32,
            device_map="cpu"
        ).eval()

        print("✅ 本地模型加载成功！可以聊天啦")

    def send_message(self, user_input, enable_search=False):
        try:
            with torch.no_grad():
                inputs = self.tokenizer(user_input, return_tensors="pt").to("cpu")
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=512,
                    do_sample=False,
                    pad_token_id=self.tokenizer.eos_token_id
                )
                response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return response, None  
        except:
            return "我在呢！你好呀～", None

    def clear_history(self):
        pass
