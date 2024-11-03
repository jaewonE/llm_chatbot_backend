# services/room.py
from sqlalchemy.orm import Session
from typing import Optional

from schemas.room import *
from model.room import RoomTable
from error.exceptions import RoomNotFoundError
from utils.converters import room_table_to_schema


class RoomService:
    def _get_room_by_id(self, db: Session, room_id: int, user_id: str) -> Optional[RoomTable]:
        return db.query(RoomTable).filter(RoomTable.id == room_id, RoomTable.user_id == user_id).first()

    def create_room(self, db: Session, create_room_input: CreateRoomInput, user_id: str) -> Room:
        create_room_input_data = create_room_input.model_dump()
        create_room_input_data["user_id"] = user_id
        room_table = RoomTable.create(create_room_input_data)
        db.add(room_table)
        db.commit()
        db.refresh(room_table)

        return room_table_to_schema(room_table)

    def get_room_by_id(self, db: Session, room_id: int, user_id: str) -> Room:
        room_table = self._get_room_by_id(db, room_id, user_id)
        if not room_table:
            raise RoomNotFoundError(f"Room with id {room_id} not found")
        return room_table_to_schema(room_table)

    def get_all_rooms_by_user(self, db: Session, user_id: str) -> list[Room]:
        room_tables = db.query(RoomTable).filter(
            RoomTable.user_id == user_id).all()
        return [room_table_to_schema(room) for room in room_tables]

    def update_room(self, db: Session, room_id: int, update_room_input: UpdateRoomInput, user_id: str) -> Room:
        room_table = self._get_room_by_id(db, room_id, user_id)
        if not room_table:
            raise RoomNotFoundError(f"Room with id {room_id} not found")

        room_table.update(**update_room_input.model_dump(exclude_unset=True))
        db.commit()
        db.refresh(room_table)

        return room_table_to_schema(room_table)

    def delete_room(self, db: Session, room_id: int, user_id: str) -> None:
        room_table = self._get_room_by_id(db, room_id, user_id)
        if not room_table:
            raise RoomNotFoundError(f"Room with id {room_id} not found")

        db.delete(room_table)
        db.commit()


room_service = RoomService()
