
from typing import Dict, Any, List, Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from .repositories import UserRepository
    from .classes import User
from .repositories import UserRepository, RoomRepository, RoomMemberRepository, MessageRepository, CallRepository, CallParticipantRepository
from .classes import Room, RoomMember, Message, Call, CallParticipant

class UserService:
    user_repo: 'UserRepository'

    def __init__(self, user_repo: 'UserRepository') -> None:
        self.user_repo = user_repo

    def delete_user(self, user_id: int) -> Optional['User']:
        return self.user_repo.soft_delete(user_id)

    def register_user(self, username: str, email: str, password: str) -> Optional['User']:
        import re
        pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!\-_.]).{8,}$'
        error = ""
        hasError = False
        try:
            if not re.match(pattern, username):
                error = "Username must be at least 8 characters, include an uppercase letter, a lowercase letter, a number, and one of !-_."
                hasError = True
            if not re.match(pattern, password):
                error = "Password must be at least 8 characters, include an uppercase letter, a lowercase letter, a number, and one of !-_."
                hasError = True
            if hasError:
                raise ValueError(error)
        except ValueError as e:
            raise e
        if not hasError:
            passwordHash = self.hash_password(password)  # type: ignore
            user = self.user_repo.create(username=username, email=email, password_hash=passwordHash)  # type: ignore
            return user
        return None

    def login_user(self, username: str, password: str) -> Optional['User']:
        try:
            user = self.user_repo.get_by_username(username)
            if not user:
                return None
            # Ensure password_hash is a string
            password_hash = user.password_hash
            if not isinstance(password_hash, str):
                password_hash = str(password_hash)
            if not self.verify_password(password, password_hash):
                return None
            # Reactivate user if soft-deleted
            if getattr(user, "status", None) == "inactive":
                setattr(user, "status", "online")
                self.user_repo.db.commit()
                self.user_repo.db.refresh(user)
            return user
        except ValueError as e:
            raise e

    def verify_password(self, password: str, password_hash: str) -> bool:
        return password == password_hash

    def get_user(self, user_id: int) -> Optional['User']:
        try:
            return self.user_repo.get_by_id(user_id)
        except ValueError as e:
            raise e

    def set_status(self, user_id: int, status: str) -> Optional['User']:
        try:
            user = self.user_repo.get_by_id(user_id)
            if not user:
                return None
            setattr(user, "status", status)
            self.user_repo.db.commit()
            self.user_repo.db.refresh(user)
            return user
        except ValueError as e:
            raise e

    def search_users(self, query: str) -> List['User']:
        try:
            users = self.user_repo.search(query)
            return users
        except ValueError as e:
            raise e

class RoomService:
    def __init__(self, room_repo: RoomRepository, room_member_repo: RoomMemberRepository, user_repo: UserRepository):
        self.room_repo = room_repo
        self.room_member_repo = room_member_repo
        self.user_repo = user_repo

    def request_to_join(self, room_id: int, user_id: int) -> Dict[str, Any]:
        member = self.room_member_repo.invite_member(room_id, user_id)
        return {"success": True, "message": "Request sent to join room.", "member": member}

    def respond_to_invite(self, room_id: int, user_id: int, accept: bool) -> Dict[str, Any]:
        member = self.room_member_repo.set_invite_response(room_id, user_id, accept)
        if accept:
            return {"success": True, "message": "Invite accepted. You can now join the room.", "member": member}
        else:
            return {"success": True, "message": "Invite rejected. You can still join later if permitted.", "member": member}

    def create_room(self, room_name: str, leader_id: int):
        import uuid
        # Generate a unique room link (could be a UUID or a URL slug)
        room_link = str(uuid.uuid4())
        room = self.room_repo.create(room_name=room_name, leader_id=leader_id, room_link=room_link)
        room_id_val = getattr(room, 'room_id', None)
        if room_id_val is not None and hasattr(room_id_val, 'value'):
            room_id_val = room_id_val.value
        if not isinstance(room_id_val, int):
            try:
                room_id_val = int(str(room_id_val))
            except Exception:
                room_id_val = leader_id
        self.room_member_repo.add_member(room_id=room_id_val, user_id=leader_id, role='leader')
        return room

    def join_room(self, room_id: int, user_id: int) -> Dict[str, Any]:
        member = self.room_member_repo.add_member(room_id=room_id, user_id=user_id)
        if not getattr(member, "is_permitted", False):
            return {"success": False, "message": "Not permitted to join. Awaiting approval.", "member": member}
        if getattr(member, "status", None) == "active":
            return {"success": True, "message": "Joined room.", "member": member}
        if getattr(member, "status", None) in ["left", "rejected"]:
            setattr(member, "status", "active")
            self.room_member_repo.db.commit()
            self.room_member_repo.db.refresh(member)
            return {"success": True, "message": "Rejoined room.", "member": member}
        return {"success": False, "message": "Unknown status.", "member": member}

    def leave_room(self, room_id: int, user_id: int) -> Dict[str, Any]:
        member = self.room_member_repo.remove_member(room_id=room_id, user_id=user_id)
        if member and getattr(member, "status", None) == "left":
            return {"success": True, "message": "Left room.", "member": member}
        return {"success": False, "message": "Not an active member or already left.", "member": member}

    def get_room(self, room_id: int):
        return self.room_repo.get_by_id(room_id)

    def list_members(self, room_id: int) -> List[RoomMember]:
        try:
            members = self.room_member_repo.get_members(room_id)
            return members if members else []
        except Exception:
            return []

    def assign_role(self, room_id: int, target_user_id: int, role: str, acting_user_id: int) -> None:
        # Only leader can assign roles
        room = self.room_repo.get_by_id(room_id)
        if room is not None and getattr(room, "leader_id", None) == acting_user_id:
            self.room_member_repo.update_role(room_id, target_user_id, role)

    def kick_user(self, room_id: int, target_user_id: int, acting_user_id: int) -> None:
        # Only leader can kick
        room = self.room_repo.get_by_id(room_id)
        if room is not None and getattr(room, "leader_id", None) == acting_user_id:
            self.room_member_repo.remove_member(room_id, target_user_id)

class MessageService:
    def __init__(self, message_repo: MessageRepository, room_member_repo: RoomMemberRepository):
        self.message_repo: MessageRepository = message_repo
        self.room_member_repo: RoomMemberRepository = room_member_repo

    def send_message(self, user_id: int, room_id: int, content: str) -> Optional[Message]:
        try:
            member = self.room_member_repo.add_member(room_id, user_id)
            if not member or not getattr(member, "is_permitted", False):
                return None
            message = self.message_repo.create(room_id=room_id, sender_id=user_id, content=content)
            return message
        except Exception:
            return None

    def get_room_messages(self, room_id: int, limit: int = 50, offset: int = 0) -> List[Message]:
        try:
            messages = self.message_repo.get_by_room(room_id, limit=limit, offset=offset)
            return messages if messages else []
        except Exception:
            return []

    def delete_message(self, message_id: int, acting_user_id: int) -> Optional[Message]:
        try:
            message = self.message_repo.db.query(Message).filter(Message.message_id == message_id).first()
            if not message:
                return None
            sender_id = getattr(message, "sender_id", None)
            if sender_id == acting_user_id:
                return self.message_repo.delete(message_id)
            room = self.room_member_repo.db.query(Room).filter(Room.room_id == getattr(message, "room_id", None)).first()
            if room is not None and getattr(room, "leader_id", None) == acting_user_id:
                return self.message_repo.delete(message_id)
            return None
        except Exception:
            return None

    def mark_as_read(self, message_id: int, user_id: int) -> Optional[Message]:
        try:
            message = self.message_repo.db.query(Message).filter(Message.message_id == message_id).first()
            if not message:
                return None
            setattr(message, "is_read", True)
            try:
                self.message_repo.db.commit()
                self.message_repo.db.refresh(message)
            except Exception:
                self.message_repo.db.rollback()
                return None
            return message
        except Exception:
            return None

class CallService:
    def __init__(self, call_repo: CallRepository, call_participant_repo: CallParticipantRepository, room_member_repo: RoomMemberRepository):
        self.call_repo: CallRepository = call_repo
        self.call_participant_repo: CallParticipantRepository = call_participant_repo
        self.room_member_repo: RoomMemberRepository = room_member_repo

    def start_call(self, room_id: int, initiator_id: int, call_type: str) -> Optional[Call]:
        try:
            member = self.room_member_repo.add_member(room_id, initiator_id)
            if not member or not getattr(member, "is_permitted", False):
                return None
            call = self.call_repo.create(room_id=room_id, initiator_id=initiator_id, call_type=call_type)
            call_id_val = getattr(call, 'call_id', None)
            if call_id_val is not None and hasattr(call_id_val, 'value'):
                call_id_val = call_id_val.value
            if not isinstance(call_id_val, int):
                try:
                    call_id_val = int(str(call_id_val))
                except Exception:
                    call_id_val = None
            if call_id_val is not None:
                self.call_participant_repo.add_participant(call_id_val, initiator_id)
            return call
        except Exception:
            return None

    def join_call(self, call_id: int, user_id: int) -> Optional[CallParticipant]:
        try:
            call = self.call_repo.db.query(Call).filter(Call.call_id == call_id).first()
            if not call:
                return None
            room_id_val = getattr(call, 'room_id', None)
            if room_id_val is not None and hasattr(room_id_val, 'value'):
                room_id_val = room_id_val.value
            if not isinstance(room_id_val, int):
                try:
                    room_id_val = int(str(room_id_val))
                except Exception:
                    room_id_val = None
            if room_id_val is None:
                return None
            member = self.room_member_repo.add_member(room_id_val, user_id)
            if not member or not getattr(member, "is_permitted", False):
                return None
            participant = self.call_participant_repo.add_participant(call_id, user_id)
            return participant
        except Exception:
            return None

    def leave_call(self, call_id: int, user_id: int) -> Optional[CallParticipant]:
        try:
            participant = self.call_participant_repo.remove_participant(call_id, user_id)
            return participant
        except Exception:
            return None

    def end_call(self, call_id: int, acting_user_id: int) -> Optional[Call]:
        try:
            call = self.call_repo.db.query(Call).filter(Call.call_id == call_id).first()
            if not call:
                return None
            room_id_val = getattr(call, 'room_id', None)
            if room_id_val is not None and hasattr(room_id_val, 'value'):
                room_id_val = room_id_val.value
            if not isinstance(room_id_val, int):
                try:
                    room_id_val = int(str(room_id_val))
                except Exception:
                    room_id_val = None
            if room_id_val is None:
                return None
            room = self.room_member_repo.db.query(Room).filter(Room.room_id == room_id_val).first()
            if room is not None and getattr(room, "leader_id", None) == acting_user_id:
                return self.call_repo.end_call(call_id)
            return None
        except Exception:
            return None

    def mute_user(self, call_id: int, target_user_id: int, acting_user_id: int) -> Optional[CallParticipant]:
        try:
            call = self.call_repo.db.query(Call).filter(Call.call_id == call_id).first()
            if not call:
                return None
            room_id_val = getattr(call, 'room_id', None)
            if room_id_val is not None and hasattr(room_id_val, 'value'):
                room_id_val = room_id_val.value
            if not isinstance(room_id_val, int):
                try:
                    room_id_val = int(str(room_id_val))
                except Exception:
                    room_id_val = None
            if room_id_val is None:
                return None
            room = self.room_member_repo.db.query(Room).filter(Room.room_id == room_id_val).first()
            if room is not None and getattr(room, "leader_id", None) == acting_user_id:
                return self.call_participant_repo.leader_mute(call_id, target_user_id, acting_user_id)
            return None
        except Exception:
            return None

    def unmute_user(self, call_id: int, target_user_id: int, acting_user_id: int) -> Optional[CallParticipant]:
        try:
            if acting_user_id != target_user_id:
                return None
            return self.call_participant_repo.user_unmute(call_id, target_user_id)
        except Exception:
            return None

    def get_call_state(self, call_id: int) -> Optional[Dict[str, Any]]:
        try:
            call = self.call_repo.db.query(Call).filter(Call.call_id == call_id).first()
            if not call:
                return None
            participants = self.call_participant_repo.get_participants(call_id)
            return {"call": call, "participants": participants}
        except Exception:
            return None