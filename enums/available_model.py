# enums/available_model.py
from enum import Enum

from error.exceptions import UnAvailableModelError


class AvailableModel(str, Enum):
    """Available models"""
    MOCK = 'Mock'


allowed_available_models = tuple(e.value for e in AvailableModel)


def str_to_available_model(model: str) -> AvailableModel:
    if model.capitalize() in allowed_available_models:
        return AvailableModel[model.capitalize()]
    raise UnAvailableModelError(f"Model {model} is not available")
