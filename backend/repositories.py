from backend.database import SessionLocal
from backend.classes import User, Room, RoomMember, Message, Call, CallParticipant
 
from sqlalchemy import or_
db = SessionLocal()

from sqlalchemy.orm import Session

class UserRepository:
    def __init__(self, db: Session):
        self.db: Session = db

    def get_by_id(self, user_id: int) -> User | None:  # type: ignore
        return self.db.query(User).filter(User.user_id == user_id).first()  # type: ignore

    def get_by_username(self, username: str) -> User | None:  # type: ignore
        return self.db.query(User).filter(User.username == username).first()  # type: ignore

    def get_all(self) -> list[User]:  # type: ignore
        return self.db.query(User).all()  # type: ignore

    def create(self, username: str, email: str, password_hash: str) -> User:  # type: ignore
        new_user = User(username=username, email=email, password_hash=password_hash)
        self.db.add(new_user)  # type: ignore
        self.db.commit()  # type: ignore
        self.db.refresh(new_user)  # type: ignore
        return new_user

    def update_status(self, user_id: int, status: str) -> User | None:  # type: ignore
        user = self.get_by_id(user_id)
        if user is not None:
            # Assign directly to SQLAlchemy field
            user.status = status  # type: ignore[attr-defined]
            try:
                self.db.commit()  # type: ignore
                self.db.refresh(user)  # type: ignore
            except Exception:
                self.db.rollback()  # type: ignore
                return None
        return user

    def soft_delete(self, user_id: int) -> User | None:  # type: ignore
        user = self.get_by_id(user_id)
        if user:
            user.status = "inactive"  # type: ignore[attr-defined]
            try:
                self.db.commit()  # type: ignore
                self.db.refresh(user)  # type: ignore
            except Exception:
                self.db.rollback()  # type: ignore
                return None
        return user
    def search(self, query: str) -> list[User]:  # type: ignore
        return self.db.query(User).filter(
            or_(User.username.ilike(f"%{query}%"), User.email.ilike(f"%{query}%"))
        ).all()  # type: ignore
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

class RoomRepository:
    def __init__(self, db: 'Session'):
        self.db: 'Session' = db

    def get_by_id(self, room_id: int) -> Room | None:  # type: ignore
        return self.db.query(Room).filter(Room.room_id == room_id).first()  # type: ignore

    def get_all(self) -> list[Room]:  # type: ignore
        return self.db.query(Room).all()  # type: ignore

    def create(self, room_name: str, leader_id: int, room_link: str = None) -> Room:  # type: ignore
        new_room = Room(room_name=room_name, leader_id=leader_id, room_link=room_link)
        self.db.add(new_room)  # type: ignore
        self.db.commit()  # type: ignore
        self.db.refresh(new_room)  # type: ignore
        return new_room

    def delete(self, room_id: int) -> Room | None:  # type: ignore
        room = self.get_by_id(room_id)
        if room:
            self.db.delete(room)  # type: ignore
            self.db.commit()  # type: ignore
        return room
class RoomMemberRepository:
    def __init__(self, db: Session):
        self.db = db

    def invite_member(self, room_id: int, user_id: int) -> RoomMember | None:  # type: ignore
        member = self.db.query(RoomMember).filter(RoomMember.room_id == room_id, RoomMember.user_id == user_id).first()  # type: ignore
        if not member:
            member = RoomMember(room_id=room_id, user_id=user_id, status="pending", is_permitted=False)
            self.db.add(member)  # type: ignore
        else:
            member.status = "pending"  # type: ignore[attr-defined]
        self.db.commit()  # type: ignore
        self.db.refresh(member)  # type: ignore
        return member

    def set_invite_response(self, room_id: int, user_id: int, accept: bool) -> RoomMember | None:  # type: ignore
        member = self.db.query(RoomMember).filter(RoomMember.room_id == room_id, RoomMember.user_id == user_id).first()  # type: ignore
        if member:
            if accept:
                member.status = "accepted"  # type: ignore[attr-defined]
                member.is_permitted = True  # type: ignore[attr-defined]
            else:
                member.status = "rejected"  # type: ignore[attr-defined]
                member.is_permitted = False  # type: ignore[attr-defined]
            self.db.commit()  # type: ignore
            self.db.refresh(member)  # type: ignore
        return member

    def ban_member(self, room_id: int, user_id: int) -> RoomMember | None:  # type: ignore
        member = self.db.query(RoomMember).filter(RoomMember.room_id == room_id, RoomMember.user_id == user_id).first()  # type: ignore
        if member:
            member.is_banned = True  # type: ignore[attr-defined]
            member.is_permitted = False  # type: ignore[attr-defined]
            member.status = "left"  # type: ignore[attr-defined]
            self.db.commit()  # type: ignore
            self.db.refresh(member)  # type: ignore
        return member

    def unban_member(self, room_id: int, user_id: int) -> RoomMember | None:  # type: ignore
        member = self.db.query(RoomMember).filter(RoomMember.room_id == room_id, RoomMember.user_id == user_id).first()  # type: ignore
        if member:
            member.is_banned = False  # type: ignore[attr-defined]
            self.db.commit()  # type: ignore
            self.db.refresh(member)  # type: ignore
        return member

    def uninvite_member(self, room_id: int, user_id: int) -> RoomMember | None:  # type: ignore
        member = self.db.query(RoomMember).filter(RoomMember.room_id == room_id, RoomMember.user_id == user_id).first()  # type: ignore
        if member:
            member.is_permitted = False  # type: ignore[attr-defined]
            member.status = "pending"  # type: ignore[attr-defined]
            self.db.commit()  # type: ignore
            self.db.refresh(member)  # type: ignore
        return member

    def add_member(self, room_id: int, user_id: int, role: str = "member") -> RoomMember:  # type: ignore
        # Check if already exists
        member = self.db.query(RoomMember).filter(RoomMember.room_id == room_id, RoomMember.user_id == user_id).first()  # type: ignore
        if member:
            if getattr(member, "is_permitted", False) and getattr(member, "status", None) in ["left", "rejected"]:  # type: ignore
                member.status = "accepted"  # type: ignore[attr-defined]
                self.db.commit()  # type: ignore
                self.db.refresh(member)  # type: ignore
                return member  # type: ignore
            return member  # Already a member or not permitted  # type: ignore
        new_member = RoomMember(room_id=room_id, user_id=user_id, role=role, status="pending", is_permitted=False)
        self.db.add(new_member)  # type: ignore
        self.db.commit()  # type: ignore
        self.db.refresh(new_member)  # type: ignore
        return new_member

    def remove_member(self, room_id: int, user_id: int) -> RoomMember | None:  # type: ignore
        member = self.db.query(RoomMember).filter(RoomMember.room_id == room_id, RoomMember.user_id == user_id).first()  # type: ignore
        if member and getattr(member, "status", None) == "active":  # type: ignore
            member.status = "left"  # type: ignore[attr-defined]
            self.db.commit()  # type: ignore
            self.db.refresh(member)  # type: ignore
        return member  # type: ignore
    def permit_member(self, room_id: int, user_id: int) -> RoomMember | None:  # type: ignore
        member = self.db.query(RoomMember).filter(RoomMember.room_id == room_id, RoomMember.user_id == user_id).first()  # type: ignore
        if member:
            member.is_permitted = True  # type: ignore[attr-defined]
            if getattr(member, "status", None) == "pending":  # type: ignore
                member.status = "active"  # type: ignore[attr-defined]
            self.db.commit()  # type: ignore
            self.db.refresh(member)  # type: ignore
        return member  # type: ignore

    def get_members(self, room_id: int) -> list[RoomMember]:  # type: ignore
        members = self.db.query(RoomMember).filter(RoomMember.room_id == room_id).all()  # type: ignore
        return members

    def get_user_rooms(self, user_id: int) -> list[RoomMember]:  # type: ignore
        rooms = self.db.query(RoomMember).filter(RoomMember.user_id == user_id).all()  # type: ignore
        return rooms

    def update_role(self, room_id: int, user_id: int, role: str) -> RoomMember | None:  # type: ignore
        member = self.db.query(RoomMember).filter(RoomMember.room_id == room_id, RoomMember.user_id == user_id).first()  # type: ignore
        if member is not None:
            member.role = role  # type: ignore[attr-defined]
            try:
                self.db.commit()  # type: ignore
                self.db.refresh(member)  # type: ignore
            except Exception:
                self.db.rollback()  # type: ignore
                return None
        return member
class MessageRepository:
    def __init__(self, db: 'Session'):
        self.db: 'Session' = db

    def create(self, room_id: int, sender_id: int, content: str) -> Message:  # type: ignore
        new_message = Message(room_id=room_id, sender_id=sender_id, content=content)
        self.db.add(new_message)  # type: ignore
        self.db.commit()  # type: ignore
        self.db.refresh(new_message)  # type: ignore
        return new_message

    def get_by_room(self, room_id: int, limit: int = 50, offset: int = 0) -> list[Message]:  # type: ignore
        messages = self.db.query(Message).filter(Message.room_id == room_id).order_by(Message.timestamp.desc()).limit(limit).offset(offset).all()  # type: ignore
        return messages

    def get_all(self) -> list[Message]:  # type: ignore
        return self.db.query(Message).all()  # type: ignore

    def delete(self, message_id: int) -> Message | None:  # type: ignore
        message = self.db.query(Message).filter(Message.message_id == message_id).first()  # type: ignore
        if message:
            self.db.delete(message)  # type: ignore
            self.db.commit()  # type: ignore
        return message
from datetime import datetime

class CallRepository:
    def __init__(self, db: 'Session'):
        self.db: 'Session' = db

    def create(self, room_id: int, initiator_id: int, call_type: str) -> Call:  # type: ignore
        new_call = Call(room_id=room_id, initiator_id=initiator_id, call_type=call_type)
        self.db.add(new_call)  # type: ignore
        self.db.commit()  # type: ignore
        self.db.refresh(new_call)  # type: ignore
        return new_call

    def end_call(self, call_id: int) -> Call | None:  # type: ignore
        call = self.db.query(Call).filter(Call.call_id == call_id).first()  # type: ignore
        if call:
            call.end_time = datetime.utcnow()  # type: ignore
            self.db.commit()  # type: ignore
            self.db.refresh(call)  # type: ignore
        return call

    def get_active_call_by_room(self, room_id: int) -> Call | None:  # type: ignore
        return self.db.query(Call).filter(Call.room_id == room_id, Call.ended_at == None).first()  # type: ignore
class CallParticipantRepository:
    def __init__(self, db: Session):
        self.db = db

    def leader_mute(self, call_id: int, user_id: int, acting_user_id: int) -> CallParticipant | None:  # type: ignore
        # Only leader can mute (assume leader check is done in service)
        participant = self.db.query(CallParticipant).filter(CallParticipant.call_id == call_id, CallParticipant.user_id == user_id).first()  # type: ignore
        if participant:
            participant.is_muted = True  # type: ignore[attr-defined]
            self.db.commit()  # type: ignore
            self.db.refresh(participant)  # type: ignore
        return participant  # type: ignore

    def user_unmute(self, call_id: int, user_id: int) -> CallParticipant | None:  # type: ignore
        participant = self.db.query(CallParticipant).filter(CallParticipant.call_id == call_id, CallParticipant.user_id == user_id).first()  # type: ignore
        if participant:
            participant.is_muted = False  # type: ignore[attr-defined]
            self.db.commit()  # type: ignore
            self.db.refresh(participant)  # type: ignore
        return participant  # type: ignore

    def add_participant(self, call_id: int, user_id: int) -> CallParticipant:  # type: ignore
        new_participant = CallParticipant(call_id=call_id, user_id=user_id)
        self.db.add(new_participant)  # type: ignore
        self.db.commit()  # type: ignore
        self.db.refresh(new_participant)  # type: ignore
        return new_participant

    def remove_participant(self, call_id: int, user_id: int) -> CallParticipant | None:  # type: ignore
        participant = self.db.query(CallParticipant).filter(CallParticipant.call_id == call_id, CallParticipant.user_id == user_id).first()  # type: ignore
        if participant:
            self.db.delete(participant)  # type: ignore
            self.db.commit()  # type: ignore
        return participant

    def get_participants(self, call_id: int) -> list[CallParticipant]:  # type: ignore
        participants = self.db.query(CallParticipant).filter(CallParticipant.call_id == call_id).all()  # type: ignore
        return participants

    def update_mute_status(self, call_id: int, user_id: int, is_muted: bool) -> CallParticipant | None:  # type: ignore
        participant = self.db.query(CallParticipant).filter(CallParticipant.call_id == call_id, CallParticipant.user_id == user_id).first()  # type: ignore
        if participant is not None:
            participant.is_muted = is_muted  # type: ignore[attr-defined]
            try:
                self.db.commit()  # type: ignore
                self.db.refresh(participant)  # type: ignore
            except Exception:
                self.db.rollback()  # type: ignore
                return None
        return participant