# apis/chat.py
from fastapi import APIRouter, Depends, Query, UploadFile, File
from sqlalchemy.orm import Session
from datetime import datetime

from auth.auth_bearer import JWTBearer
from services.chat import chat_service
from schemas.chat import *
from db import get_db_session
from error.exceptions import *
from error.handler import handle_http_exceptions

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
    responses={404: {"description": "Not found"}},
)


@router.post("/create", dependencies=[Depends(JWTBearer())], response_model=CreateChatOutput)
@handle_http_exceptions
async def create_chat_endpoint(
        create_chat_input: CreateChatInput,
        db: Session = Depends(get_db_session),
        user_id: str = Depends(JWTBearer())) -> CreateChatOutput:
    chat = await chat_service.create_chat(db, create_chat_input, user_id)
    return CreateChatOutput(chat=chat, success=True, message="Chat created successfully")


@router.get("/chat/{chat_id}", dependencies=[Depends(JWTBearer())], response_model=GetChatOutput)
@handle_http_exceptions
def get_chat_endpoint(
        chat_id: int,
        db: Session = Depends(get_db_session),
        user_id: str = Depends(JWTBearer())) -> GetChatOutput:
    chat = chat_service.get_chat_by_id(db, chat_id, user_id)
    return GetChatOutput(chat=chat, success=True, message="Chat fetched successfully")


@router.get("/room/{room_id}", dependencies=[Depends(JWTBearer())], response_model=GetRoomChatsOutput)
@handle_http_exceptions
def get_room_chats_endpoint(
        room_id: int,
        db: Session = Depends(get_db_session),
        user_id: str = Depends(JWTBearer())) -> GetRoomChatsOutput:
    room = chat_service.get_all_chats_by_room(db, room_id, user_id)
    return GetRoomChatsOutput(room=room, success=True, message="Chats fetched successfully")


@router.put("/update/{chat_id}", dependencies=[Depends(JWTBearer())], response_model=UpdateChatOutput)
@handle_http_exceptions
def update_chat_endpoint(
        chat_id: int,
        update_chat_input: UpdateChatInput,
        db: Session = Depends(get_db_session),
        user_id: str = Depends(JWTBearer())) -> UpdateChatOutput:
    chat = chat_service.update_chat(
        db, chat_id, update_chat_input, user_id)
    return UpdateChatOutput(chat=chat, success=True, message="Chat updated successfully")


@router.delete("/delete/{chat_id}", dependencies=[Depends(JWTBearer())], response_model=DeleteChatOutput)
@handle_http_exceptions
def delete_chat_endpoint(
        chat_id: int,
        db: Session = Depends(get_db_session),
        user_id: str = Depends(JWTBearer())) -> DeleteChatOutput:
    chat_service.delete_chat(db, chat_id, user_id)
    return DeleteChatOutput(success=True, message="Chat deleted successfully")
