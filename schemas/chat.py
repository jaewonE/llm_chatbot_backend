# schemas/chat.py
from pydantic import BaseModel, field_validator
from typing import Optional, List
from datetime import datetime

from schemas.common import BaseOutput
from schemas.room import Room
from validator.chat import validate_model


class Chat(BaseModel):
    id: str
    room_id: str
    ask: str
    answer: str
    model: str
    timestamp: datetime

    class Config:
        from_attributes = True
        use_enum_values = True

    _validate_model = field_validator('model')(validate_model)


class CreateChatInput(BaseModel):
    room_id: Optional[str] = None
    model: Optional[str] = None
    ask: str

    _validate_model = field_validator('model')(validate_model)


class CreateChatOutput(BaseOutput):
    chat: Optional[Chat] = None


class GetChatOutput(BaseOutput):
    chat: Optional[Chat] = None


class GetRoomChatsOutput(BaseOutput):
    room: Optional[Room] = None


class UpdateChatInput(BaseModel):
    id: str
    model: str
    ask: str

    _validate_model = field_validator('model')(
        lambda cls, v: validate_model(v) if v is not None else v)


class UpdateChatOutput(BaseOutput):
    chat: Optional[Chat] = None


class DeleteChatOutput(BaseOutput):
    pass  # No additional fields needed
