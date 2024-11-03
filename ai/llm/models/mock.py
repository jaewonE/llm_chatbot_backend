from time import sleep
from ai.llm.models.interface.base_ai_model import BaseAiModel


class MockModel(BaseAiModel):
    def __init__(self, max_length=30, delay=3, init_delay=2, model_name="MockModel"):
        self.max_length = max_length
        self.delay = delay
        sleep(init_delay)
        print(f"Load {model_name} model complete.")

    def generate_response(self, prompt, messages=[]):
        sleep(self.delay)
        return f"Mock response to {prompt}"

    def set_max_length(self, max_length):
        self.max_length = max_length
