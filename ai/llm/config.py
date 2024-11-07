from dataclasses import dataclass
from typing import Type, Dict, Any

from enums.available_model import AvailableModel
from ai.llm.models import MockModel, MentalLlm


@dataclass
class ModelConfig:
    model_cls: Type
    args: Dict[str, Any]


model_dict = {
    AvailableModel.MOCK.value: ModelConfig(
        model_cls=MockModel,
        args={'model_name': "Mock", 'delay': 3, 'init_delay': 3}
    ),
    AvailableModel.MentalLlm.value: ModelConfig(
        model_cls=MentalLlm,
        args={'model_name': "MentalLlm"}
    ),
    # AvailableModel.GEMMA.value: ModelConfig(
    #     model_cls=GemmaModel,
    #     args={'model_name': 'Gemma', 'max_length': 128}
    # ),
    # AvailableModel.LLAMA2.value: ModelConfig(
    #     model_cls=LLama2Model,
    #     args={'model_name': 'LLama2', 'max_length': 512, 'device': 'cuda'}
    # ),
}
