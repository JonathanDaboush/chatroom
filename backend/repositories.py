
from backend.classes import User, Room, RoomMember, Message, Call, CallParticipant
from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.db.execute(select(User).where(User.user_id == user_id))
        return result.scalars().first()

    async def get_by_username(self, username: str) -> User | None:
        result = await self.db.execute(select(User).where(User.username == username))
        return result.scalars().first()

    async def get_all(self) -> list[User]:
        result = await self.db.execute(select(User))
        return list(result.scalars().all())

    async def create(self, username: str, email: str, password_hash: str) -> User:
        new_user = User(username=username, email=email, password_hash=password_hash)
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user

    async def update_status(self, user_id: int, status: str) -> User | None:
        user = await self.get_by_id(user_id)
        if user is not None:
            setattr(user, "status", status)
            try:
                await self.db.commit()
                await self.db.refresh(user)
            except Exception:
                await self.db.rollback()
                return None
        return user

    async def soft_delete(self, user_id: int) -> User | None:
        user = await self.get_by_id(user_id)
        if user:
            setattr(user, "status", "inactive")
            try:
                await self.db.commit()
                await self.db.refresh(user)
            except Exception:
                await self.db.rollback()
                return None
        return user

    async def search(self, query: str) -> list[User]:
        result = await self.db.execute(
            select(User).where(
                or_(User.username.ilike(f"%{query}%"), User.email.ilike(f"%{query}%"))
            )
        )
        return list(result.scalars().all())


class RoomRepository:
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def get_by_id(self, room_id: int) -> Room | None:
        result = await self.db.execute(select(Room).where(Room.room_id == room_id))
        return result.scalars().first()

    async def get_all(self) -> list[Room]:
        result = await self.db.execute(select(Room))
        return list(result.scalars().all())

    async def create(self, room_name: str, leader_id: int, room_link: str | None = None) -> Room:
        new_room = Room(room_name=room_name, leader_id=leader_id, room_link=room_link)
        self.db.add(new_room)
        await self.db.commit()
        await self.db.refresh(new_room)
        return new_room

    async def delete(self, room_id: int) -> Room | None:
        room = await self.get_by_id(room_id)
        if room:
            await self.db.delete(room)
            await self.db.commit()
        return room

    async def get_by_id_by_link(self, room_link: str) -> Room | None:
        result = await self.db.execute(select(Room).where(Room.room_link == room_link))
        return result.scalars().first()
class RoomMemberRepository:
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def get_member(self, room_id: int, user_id: int) -> RoomMember | None:
        result = await self.db.execute(select(RoomMember).where(RoomMember.room_id == room_id, RoomMember.user_id == user_id))
        return result.scalars().first()

    async def invite_member(self, room_id: int, user_id: int) -> RoomMember | None:
        result = await self.db.execute(select(RoomMember).where(RoomMember.room_id == room_id, RoomMember.user_id == user_id))
        member = result.scalars().first()
        if not member:
            member = RoomMember(room_id=room_id, user_id=user_id, status="pending", is_permitted=False)
            self.db.add(member)
        else:
            setattr(member, "status", "pending")
        await self.db.commit()
        await self.db.refresh(member)
        return member

    async def set_invite_response(self, room_id: int, user_id: int, accept: bool) -> RoomMember | None:
        result = await self.db.execute(select(RoomMember).where(RoomMember.room_id == room_id, RoomMember.user_id == user_id))
        member = result.scalars().first()
        if member:
            if accept:
                setattr(member, "status", "accepted")
                setattr(member, "is_permitted", True)
            else:
                setattr(member, "status", "rejected")
                setattr(member, "is_permitted", False)
            await self.db.commit()
            await self.db.refresh(member)
        return member

    async def ban_member(self, room_id: int, user_id: int) -> RoomMember | None:
        result = await self.db.execute(select(RoomMember).where(RoomMember.room_id == room_id, RoomMember.user_id == user_id))
        member = result.scalars().first()
        if member:
            setattr(member, "is_banned", True)
            setattr(member, "is_permitted", False)
            setattr(member, "status", "left")
            await self.db.commit()
            await self.db.refresh(member)
        return member

    async def unban_member(self, room_id: int, user_id: int) -> RoomMember | None:
        result = await self.db.execute(select(RoomMember).where(RoomMember.room_id == room_id, RoomMember.user_id == user_id))
        member = result.scalars().first()
        if member:
            setattr(member, "is_banned", False)
            await self.db.commit()
            await self.db.refresh(member)
        return member

    async def uninvite_member(self, room_id: int, user_id: int) -> RoomMember | None:
        result = await self.db.execute(select(RoomMember).where(RoomMember.room_id == room_id, RoomMember.user_id == user_id))
        member = result.scalars().first()
        if member:
            setattr(member, "is_permitted", False)
            setattr(member, "status", "pending")
            await self.db.commit()
            await self.db.refresh(member)
        return member

    async def add_member(self, room_id: int, user_id: int, role: str = "member") -> RoomMember:
        result = await self.db.execute(select(RoomMember).where(RoomMember.room_id == room_id, RoomMember.user_id == user_id))
        member = result.scalars().first()
        if member:
            if getattr(member, "is_permitted", False) and getattr(member, "status", None) in ["left", "rejected"]:
                setattr(member, "status", "accepted")
                await self.db.commit()
                await self.db.refresh(member)
                return member
            return member
        new_member = RoomMember(room_id=room_id, user_id=user_id, role=role, status="pending", is_permitted=False)
        self.db.add(new_member)
        await self.db.commit()
        await self.db.refresh(new_member)
        return new_member

    async def remove_member(self, room_id: int, user_id: int) -> RoomMember | None:
        result = await self.db.execute(select(RoomMember).where(RoomMember.room_id == room_id, RoomMember.user_id == user_id))
        member = result.scalars().first()
        if member and getattr(member, "status", None) == "active":
            setattr(member, "status", "left")
            await self.db.commit()
            await self.db.refresh(member)
        return member
    async def permit_member(self, room_id: int, user_id: int) -> RoomMember | None:
        result = await self.db.execute(select(RoomMember).where(RoomMember.room_id == room_id, RoomMember.user_id == user_id))
        member = result.scalars().first()
        if member:
            setattr(member, "is_permitted", True)
            if getattr(member, "status", None) == "pending":
                setattr(member, "status", "active")
            await self.db.commit()
            await self.db.refresh(member)
        return member

    async def get_members(self, room_id: int) -> list[RoomMember]:
        result = await self.db.execute(select(RoomMember).where(RoomMember.room_id == room_id))
        return list(result.scalars().all())

    async def get_user_rooms(self, user_id: int) -> list[RoomMember]:
        result = await self.db.execute(select(RoomMember).where(RoomMember.user_id == user_id))
        return list(result.scalars().all())

    async def update_role(self, room_id: int, user_id: int, role: str) -> RoomMember | None:
        result = await self.db.execute(select(RoomMember).where(RoomMember.room_id == room_id, RoomMember.user_id == user_id))
        member = result.scalars().first()
        if member is not None:
            setattr(member, "role", role)
            try:
                await self.db.commit()
                await self.db.refresh(member)
            except Exception:
                await self.db.rollback()
                return None
        return member
class MessageRepository:
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def get_by_id(self, message_id: int) -> Message | None:
        result = await self.db.execute(select(Message).where(Message.message_id == message_id))
        return result.scalars().first()

    async def create(self, room_id: int, sender_id: int, content: str) -> Message:
        new_message = Message(room_id=room_id, sender_id=sender_id, content=content)
        self.db.add(new_message)
        await self.db.commit()
        await self.db.refresh(new_message)
        return new_message

    async def update_message(self, message_id: int, new_content: str) -> Message | None:
        result = await self.db.execute(select(Message).where(Message.message_id == message_id))
        message = result.scalars().first()
        if message:
            setattr(message, "content", new_content)
            await self.db.commit()
            await self.db.refresh(message)
        return message

    async def create_reply(self, room_id: int, sender_id: int, parent_message_id: int, content: str) -> Message:
        new_message = Message(room_id=room_id, sender_id=sender_id, content=content, parent_message_id=parent_message_id)
        self.db.add(new_message)
        await self.db.commit()
        await self.db.refresh(new_message)
        return new_message

    async def get_by_room(self, room_id: int, limit: int = 50, offset: int = 0) -> list[Message]:
        result = await self.db.execute(
            select(Message).where(Message.room_id == room_id).order_by(Message.timestamp.desc()).limit(limit).offset(offset)
        )
        return list(result.scalars().all())

    async def get_all(self) -> list[Message]:
        result = await self.db.execute(select(Message))
        return list(result.scalars().all())

    async def delete(self, message_id: int) -> Message | None:
        result = await self.db.execute(select(Message).where(Message.message_id == message_id))
        message = result.scalars().first()
        if message:
            await self.db.delete(message)
            await self.db.commit()
        return message


class CallRepository:
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def create(self, room_id: int, initiator_id: int, call_type: str) -> Call:
        new_call = Call(room_id=room_id, initiator_id=initiator_id, call_type=call_type)
        self.db.add(new_call)
        await self.db.commit()
        await self.db.refresh(new_call)
        return new_call

    async def end_call(self, call_id: int) -> Call | None:
        result = await self.db.execute(select(Call).where(Call.call_id == call_id))
        call = result.scalars().first()
        if call:
            from datetime import datetime, timezone
            setattr(call, "ended_at", datetime.now(timezone.utc))
            await self.db.commit()
            await self.db.refresh(call)
        return call

    async def get_active_call_by_room(self, room_id: int) -> Call | None:
        result = await self.db.execute(select(Call).where(Call.room_id == room_id, Call.ended_at == None))
        return result.scalars().first()

    async def get_latest_call_by_room(self, room_id: int) -> Call | None:
        result = await self.db.execute(
            select(Call).where(Call.room_id == room_id).order_by(Call.started_at.desc())
        )
        return result.scalars().first()
class CallParticipantRepository:
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def leader_mute(self, call_id: int, user_id: int, acting_user_id: int) -> CallParticipant | None:
        result = await self.db.execute(select(CallParticipant).where(CallParticipant.call_id == call_id, CallParticipant.user_id == user_id))
        participant = result.scalars().first()
        if participant:
            setattr(participant, "is_muted", True)
            await self.db.commit()
            await self.db.refresh(participant)
        return participant

    async def user_unmute(self, call_id: int, user_id: int) -> CallParticipant | None:
        result = await self.db.execute(select(CallParticipant).where(CallParticipant.call_id == call_id, CallParticipant.user_id == user_id))
        participant = result.scalars().first()
        if participant:
            setattr(participant, "is_muted", False)
            await self.db.commit()
            await self.db.refresh(participant)
        return participant

    async def add_participant(self, call_id: int, user_id: int) -> CallParticipant:
        new_participant = CallParticipant(call_id=call_id, user_id=user_id)
        self.db.add(new_participant)
        await self.db.commit()
        await self.db.refresh(new_participant)
        return new_participant

    async def remove_participant(self, call_id: int, user_id: int) -> CallParticipant | None:
        result = await self.db.execute(select(CallParticipant).where(CallParticipant.call_id == call_id, CallParticipant.user_id == user_id))
        participant = result.scalars().first()
        if participant:
            await self.db.delete(participant)
            await self.db.commit()
        return participant

    async def get_participants(self, call_id: int) -> list[CallParticipant]:
        result = await self.db.execute(select(CallParticipant).where(CallParticipant.call_id == call_id))
        return list(result.scalars().all())

    async def update_mute_status(self, call_id: int, user_id: int, is_muted: bool) -> CallParticipant | None:
        result = await self.db.execute(select(CallParticipant).where(CallParticipant.call_id == call_id, CallParticipant.user_id == user_id))
        participant = result.scalars().first()
        if participant is not None:
            setattr(participant, "is_muted", is_muted)
            try:
                await self.db.commit()
                await self.db.refresh(participant)
            except Exception:
                await self.db.rollback()
                return None
        return participant