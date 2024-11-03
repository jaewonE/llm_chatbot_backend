from abc import ABC, abstractmethod


class BaseAiModel(ABC):
    """Model interface for AI models"""

    @abstractmethod
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def generate_response(self, prompt: str, messages=[]) -> str:
        pass

    @abstractmethod
    def set_max_length(self, max_length: int) -> None:
        pass
