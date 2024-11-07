from time import sleep
import torch
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer

from ai.llm.models.interface.base_ai_model import BaseAiModel
from log import logger


class MentalLlm(BaseAiModel):
    def __init__(self, max_length=512, model_name="MentalLlm"):
        self.max_length = max_length
        self.user_name = "사용자"

        # 모델과 토크나이저 로드
        load_model_name = "juhoon01/ko_llama3_model_shinhan_2"
        self.model = AutoModelForCausalLM.from_pretrained(
            load_model_name, torch_dtype=torch.float32, device_map="None")
        self.tokenizer = AutoTokenizer.from_pretrained(load_model_name)

        logger.info(f"Load {model_name} model complete.")

    def preProcess(self, text: str) -> str:
        """ LLM에 입력하기 전에 전처리를 수행"""
        return text

    def postProcess(self, text: str) -> str:
        """ LLM의 출력을 후처리"""
        text = text['generated_text'].replace("사우", f"{self.user_name}")
        return text

    def generate_response(self, prompt: str, messages=[]):
        """
        prompt(str): 사용자의 입력
            - EX: prompt = "요즘 무기력하고 힘들어요. 에너지가 없어서 아무것도 하기 싫은 기분이 많이 들어요"
        messages(list): 사용자와의 이전 대화 내용
        """
        # LLM에 입력하기 전에 전처리를 수행
        prompt = self.preProcess(prompt)

        pipe = pipeline(task="text-generation", model=self.model,
                        tokenizer=self.tokenizer, max_length=self.max_length)
        result = pipe(f"### 질문: {prompt}\n### 답변:")

        # LLM의 출력을 후처리
        return self.postProcess(result[0])

    def set_max_length(self, max_length):
        self.max_length = max_length
