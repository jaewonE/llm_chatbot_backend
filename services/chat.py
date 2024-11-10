# services/chat.py
from sqlalchemy.orm import Session, joinedload
from datetime import datetime
from typing import Optional

from schemas.chat import *
from ai.llm import load_llm_model, generate_response
from schemas.room import CreateRoomInput, Room
from model.chat import ChatTable
from model.room import RoomTable
from error.exceptions import ChatNotFoundError, UnauthorizedError
from utils.converters import chat_table_to_schema, room_table_to_schema
from services.room import room_service
from ai.llm.config import AvailableModel, str_to_available_model
from ai.rag import rag_service


class ChatService:
    def _get_user_room(self, db: Session, room_id: int, user_id: str) -> Optional[RoomTable]:
        return db.query(RoomTable).filter(
            RoomTable.id == room_id,
            RoomTable.user_id == user_id
        ).first()

    async def create_chat(self, db: Session, create_chat_input: CreateChatInput, user_id: str) -> Chat:
        if create_chat_input.room_id == None:
            room = room_service.create_room(db, CreateRoomInput(), user_id)
            create_chat_input.room_id = room.id
        else:
            room = self._get_user_room(db, create_chat_input.room_id, user_id)
            if room.user_id != user_id:
                raise UnauthorizedError(
                    "You are not authorized to create a chat for this room")

        print("ASK:", create_chat_input.ask)
        rag_responses = rag_service.search_in_rag(create_chat_input.ask)
        print("RAG RESPONSES:", rag_responses)
        rag_prompt = create_chat_input.ask
        for i in range(len(rag_responses)):
            rag_prompt += f"{i+1}. {rag_responses[i]}\n"

        if create_chat_input.model == None:
            create_chat_input.model = AvailableModel.MOCK.value
        use_model = str_to_available_model(create_chat_input.model)

        # LLM 모델 로드 및 응답 생성
        load_llm_model(use_model)  # 이미 모델이 로드 되어있으면 로드하지 않음.
        response = generate_response(use_model, rag_prompt)

        create_chat_data = create_chat_input.model_dump()
        create_chat_data['answer'] = response
        create_chat_data['timestamp'] = datetime.now()

        chat_table = ChatTable(**create_chat_data)
        db.add(chat_table)
        db.commit()
        db.refresh(chat_table)

        return chat_table_to_schema(chat_table)

    def get_chat_by_id(self, db: Session, chat_id: int, user_id: str) -> Chat:
        chat_table = db.query(ChatTable).join(RoomTable).filter(
            ChatTable.id == chat_id,
            RoomTable.user_id == user_id
        ).first()
        if not chat_table:
            raise ChatNotFoundError(f"Chat with id {chat_id} not found")
        return chat_table_to_schema(chat_table)

    def get_all_chats_by_room(self, db: Session, room_id: str, user_id: str) -> Room:
        room = db.query(RoomTable).options(joinedload(RoomTable.chats)).filter(
            RoomTable.id == room_id,
            RoomTable.user_id == user_id
        ).first()

        if not room:
            raise UnauthorizedError(
                "You are not authorized to view chats for this room")

        return room_table_to_schema(room)

    def update_chat(self, db: Session, chat_id: int, update_chat_input: UpdateChatInput, user_id: str) -> Chat:
        chat_table = db.query(ChatTable).join(RoomTable).filter(
            ChatTable.id == chat_id,
            RoomTable.user_id == user_id
        ).first()
        if not chat_table:
            raise UnauthorizedError(
                "You are not authorized to view chats for this room")

        # LLM 모델 로드 및 응답 생성
        use_model = str_to_available_model(update_chat_input.model)
        load_llm_model(use_model)
        response = generate_response(use_model, update_chat_input.ask)

        update_chat_data = update_chat_input.model_dump()
        update_chat_data['answer'] = response
        update_chat_data['timestamp'] = datetime.now()
        update_chat_data['room_id'] = chat_table.room_id

        chat_table.update(**update_chat_data)
        db.commit()
        db.refresh(chat_table)

        return chat_table_to_schema(chat_table)

    def delete_chat(self, db: Session, chat_id: int, user_id: str) -> None:
        chat_table = db.query(ChatTable).join(RoomTable).filter(
            ChatTable.id == chat_id,
            RoomTable.user_id == user_id
        ).first()
        if not chat_table:
            raise ChatNotFoundError(f"Chat with id {chat_id} not found")

        db.delete(chat_table)
        db.commit()


chat_service = ChatService()
