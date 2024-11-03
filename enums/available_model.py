# enums/available_model.py
from enum import Enum

from error.exceptions import UnAvailableModelError


class AvailableModel(str, Enum):
    """Available models"""
    MOCK = 'Mock'


allowed_available_models = tuple(e.value for e in AvailableModel)


def str_to_available_model(model: str) -> AvailableModel:
    capitalized_model = model.capitalize()
    if capitalized_model in allowed_available_models:
        return AvailableModel(capitalized_model)
    raise UnAvailableModelError(f"Model {model} is not available")
