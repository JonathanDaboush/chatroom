from typing import Dict, Any, List, Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from .repositories import UserRepository
    from .classes import User

from .repositories import UserRepository, RoomRepository, RoomMemberRepository, MessageRepository, CallRepository, CallParticipantRepository
from .classes import RoomMember, Message, Call, CallParticipant
from . import email as email_module

import asyncio


class UserService:
    user_repo: 'UserRepository'

    def __init__(self, user_repo: 'UserRepository') -> None:
        """
        Purpose: Initializes the UserService with a user repository.
        Inputs: user_repo (UserRepository)
        Outputs: None.
        """
        self.user_repo = user_repo

    async def delete_user(self, user_id: int) -> Optional['User']:
        """
        Purpose: Soft deletes a user and sends a deletion email.
        Inputs: user_id (int)
        Outputs: Deleted User object or None.
        """
        user: Optional['User'] = await self.user_repo.soft_delete(user_id)
        if user is not None and hasattr(user, 'email') and hasattr(user, 'username'):
            try:
                await asyncio.to_thread(email_module.send_html_email,
                    to_email=str(user.email),
                    subject="Account Deleted",
                    context={"username": str(user.username)},
                    template_type="delete_account"
                )
            except Exception:
                pass
        return user

    async def register_user(self, username: str, email: str, password: str) -> Optional['User']:
        """
        Purpose: Registers a new user after validating credentials and sends a welcome email.
        Inputs: username (str), email (str), password (str)
        Outputs: Created User object or None.
        """
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
            passwordHash: str = self.hash_password(password)  # type: ignore
            user: Optional['User'] = await self.user_repo.create(username=username, email=email, password_hash=passwordHash)  # type: ignore
            try:
                await asyncio.to_thread(email_module.send_html_email,
                    to_email=str(email),
                    subject="Welcome to Chatroom!",
                    context={"username": str(username)},
                    template_type="new_user"
                )
            except Exception:
                pass
            return user
        return None

    async def forgot_password(self, email: str) -> bool:
        """
        Purpose: Sends a password reset email if the user exists.
        Inputs: email (str)
        Outputs: True if email sent, else False.
        """
        user: Optional['User'] = await self.user_repo.get_by_username(email)
        if not user or not hasattr(user, 'username'):
            return False
        try:
            await asyncio.to_thread(email_module.send_html_email,
                to_email=str(email),
                subject="Password Reset Request",
                context={"username": str(user.username)},
                template_type="forgot_password"
            )
            return True
        except Exception:
            return False

    async def login_user(self, username: str, password: str) -> Optional['User']:
        """
        Purpose: Authenticates a user and updates their status to online.
        Inputs: username (str), password (str)
        Outputs: User object if credentials are valid, else None.
        """
        try:
            user: Optional['User'] = await self.user_repo.get_by_username(username)
            if not user or not hasattr(user, 'password_hash'):
                return None
            password_hash: str = str(user.password_hash)
            if not self.verify_password(password, password_hash):
                return None
            if getattr(user, "status", None) == "inactive":
                setattr(user, "status", "online")
                await self.user_repo.db.commit()
                await self.user_repo.db.refresh(user)
            return user
        except ValueError as e:
            raise e

    def verify_password(self, password: str, password_hash: str) -> bool:
        """
        Purpose: Verifies a password against its hash.
        Inputs: password (str), password_hash (str)
        Outputs: True if match, else False.
        """
        return password == password_hash

    async def get_user(self, user_id: int) -> Optional['User']:
        """
        Purpose: Retrieves a user by their ID.
        Inputs: user_id (int)
        Outputs: User object or None.
        """
        try:
            user: Optional['User'] = await self.user_repo.get_by_id(user_id)
            return user
        except ValueError as e:
            raise e

    async def set_status(self, user_id: int, status: str) -> Optional['User']:
        """
        Purpose: Sets the status of a user (e.g., online, inactive).
        Inputs: user_id (int), status (str)
        Outputs: Updated User object or None.
        """
        try:
            user: Optional['User'] = await self.user_repo.get_by_id(user_id)
            if not user:
                return None
            setattr(user, "status", status)
            await self.user_repo.db.commit()
            await self.user_repo.db.refresh(user)
            return user
        except ValueError as e:
            raise e

    async def search_users(self, query: str) -> List['User']:
        """
        Purpose: Searches for users matching a query string.
        Inputs: query (str)
        Outputs: List of User objects.
        """
        try:
            users: List['User'] = await self.user_repo.search(query)
            return users
        except ValueError as e:
            raise e


class RoomService:
    def __init__(self, room_repo: RoomRepository, room_member_repo: RoomMemberRepository, user_repo: UserRepository):
        """
        Purpose: Initializes the RoomService with repositories for rooms, members, and users.
        Inputs: room_repo, room_member_repo, user_repo
        Outputs: None.
        """
        self.room_repo = room_repo
        self.room_member_repo = room_member_repo
        self.user_repo = user_repo

    async def request_to_join(self, room_id: int, user_id: int) -> Dict[str, Any]:
        """
        Purpose: Handles a user's request to join a room.
        Inputs: room_id (int), user_id (int)
        Outputs: Dict with success status, message, and member info.
        """
        # User requests to join a room (self-invite)
        member = await self.room_member_repo.get_member(room_id, user_id)
        if member:
            if getattr(member, "status", None) == "active":
                return {"success": False, "message": "Already a member.", "member": member}
            if getattr(member, "status", None) == "pending":
                return {"success": False, "message": "Already requested to join.", "member": member}
        member = await self.room_member_repo.invite_member(room_id, user_id)
        return {"success": True, "message": "Request sent to join room.", "member": member}

    async def respond_to_invite(self, room_id: int, user_id: int, accept: bool) -> Dict[str, Any]:
        """
        Purpose: Handles a user's response to a room invite.
        Inputs: room_id (int), user_id (int), accept (bool)
        Outputs: Dict with success status, message, and member info.
        """
        # User responds to an invite (accept/reject)
        member = await self.room_member_repo.set_invite_response(room_id, user_id, accept)
        if accept:
            return {"success": True, "message": "Invite accepted. You can now join the room.", "member": member}
        else:
            return {"success": True, "message": "Invite rejected. You can still join later if permitted.", "member": member}

    async def create_room(self, room_name: str, leader_id: int):
        """
        Purpose: Creates a new room and assigns the leader.
        Inputs: room_name (str), leader_id (int)
        Outputs: Created Room object.
        """
        import uuid
        # Generate a unique room link (could be a UUID or a URL slug)
        room_link = str(uuid.uuid4())
        room = await self.room_repo.create(room_name=room_name, leader_id=leader_id, room_link=room_link)
        room_id_val = getattr(room, 'room_id', None)
        if room_id_val is not None and hasattr(room_id_val, 'value'):
            room_id_val = room_id_val.value
        if not isinstance(room_id_val, int):
            try:
                room_id_val = int(str(room_id_val))
            except Exception:
                room_id_val = leader_id
        await self.room_member_repo.add_member(room_id=room_id_val, user_id=leader_id, role='leader')
        return room

    async def join_room(self, room_id: int, user_id: int) -> Dict[str, Any]:
        """
        Purpose: Handles a user joining a room, including rejoining and permission checks.
        Inputs: room_id (int), user_id (int)
        Outputs: Dict with success status, message, and member info.
        """
        # User joins a room (must be permitted)
        member = await self.room_member_repo.get_member(room_id, user_id)
        if member:
            if getattr(member, "is_banned", False):
                return {"success": False, "message": "You are banned from this room.", "member": member}
            if getattr(member, "is_permitted", False):
                if getattr(member, "status", None) in ["left", "rejected"]:
                    # Rejoin
                    setattr(member, "status", "active")
                    await self.room_member_repo.db.commit()
                    await self.room_member_repo.db.refresh(member)
                    return {"success": True, "message": "Rejoined room.", "member": member}
                if getattr(member, "status", None) == "active":
                    return {"success": False, "message": "Already a member.", "member": member}
                # Accept invite
                setattr(member, "status", "active")
                await self.room_member_repo.db.commit()
                await self.room_member_repo.db.refresh(member)
                return {"success": True, "message": "Joined room.", "member": member}
            else:
                return {"success": False, "message": "Not permitted to join. Awaiting approval.", "member": member}
        # Not a member yet, create as pending
        member = await self.room_member_repo.invite_member(room_id, user_id)
        return {"success": False, "message": "Request sent to join room. Awaiting approval.", "member": member}

    async def leave_room(self, room_id: int, user_id: int) -> Dict[str, Any]:
        """
        Purpose: Handles a user leaving a room.
        Inputs: room_id (int), user_id (int)
        Outputs: Dict with success status, message, and member info.
        """
        member = await self.room_member_repo.get_member(room_id, user_id)
        if not member or getattr(member, "status", None) != "active":
            return {"success": False, "message": "Not an active member or already left.", "member": member}
        await self.room_member_repo.remove_member(room_id, user_id)
        return {"success": True, "message": "Left room.", "member": member}

    async def get_room(self, room_id: int):
        """
        Purpose: Retrieves a room by its ID.
        Inputs: room_id (int)
        Outputs: Room object or None.
        """
        return await self.room_repo.get_by_id(room_id)

    async def list_members(self, room_id: int) -> List[RoomMember]:
        """
        Purpose: Lists all members of a room.
        Inputs: room_id (int)
        Outputs: List of RoomMember objects.
        """
        try:
            members = await self.room_member_repo.get_members(room_id)
            return members if members else []
        except Exception:
            return []

    async def assign_role(self, room_id: int, target_user_id: int, role: str, acting_user_id: int) -> None:
        """
        Purpose: Assigns a role to a user in a room (leader only).
        Inputs: room_id (int), target_user_id (int), role (str), acting_user_id (int)
        Outputs: None.
        """
        # Only leader can assign roles
        room = await self.room_repo.get_by_id(room_id)
        if room is not None and getattr(room, "leader_id", None) == acting_user_id:
            await self.room_member_repo.update_role(room_id, target_user_id, role)

    async def kick_user(self, room_id: int, target_user_id: int, acting_user_id: int) -> None:
        """
        Purpose: Removes a user from a room (leader only).
        Inputs: room_id (int), target_user_id (int), acting_user_id (int)
        Outputs: None.
        """
        # Only leader can kick
        room = await self.room_repo.get_by_id(room_id)
        if room is not None and getattr(room, "leader_id", None) == acting_user_id:
            await self.room_member_repo.remove_member(room_id, target_user_id)


class MessageService:
    def __init__(self, message_repo: MessageRepository, room_member_repo: RoomMemberRepository):
        """
        Purpose: Initializes the MessageService with message and room member repositories.
        Inputs: message_repo, room_member_repo
        Outputs: None.
        """
        self.message_repo: MessageRepository = message_repo
        self.room_member_repo: RoomMemberRepository = room_member_repo

    async def send_message(self, user_id: int, room_id: int, content: str) -> Optional[Message]:
        """
        Purpose: Sends a message to a room if the user is permitted.
        Inputs: user_id (int), room_id (int), content (str)
        Outputs: Created Message object or None.
        """
        try:
            member = await self.room_member_repo.add_member(room_id, user_id)
            if not member or not getattr(member, "is_permitted", False):
                return None
            message = await self.message_repo.create(room_id=room_id, sender_id=user_id, content=content)
            return message
        except Exception:
            return None

    async def get_room_messages(self, room_id: int, limit: int = 50, offset: int = 0) -> List[Message]:
        """
        Purpose: Retrieves messages for a room with pagination.
        Inputs: room_id (int), limit (int), offset (int)
        Outputs: List of Message objects.
        """
        try:
            messages = await self.message_repo.get_by_room(room_id, limit=limit, offset=offset)
            return messages if messages else []
        except Exception:
            return []

    async def delete_message(self, message_id: int, acting_user_id: int) -> Optional[Message]:
        """
        Purpose: Deletes a message if the acting user is the sender or room leader.
        Inputs: message_id (int), acting_user_id (int)
        Outputs: Deleted Message object or None.
        """
        try:
            message = await self.message_repo.get_by_id(message_id)
            if not message:
                return None
            sender_id = getattr(message, "sender_id", None)
            if sender_id == acting_user_id:
                return await self.message_repo.delete(message_id)
            room_id = getattr(message, "room_id", None)
            room = await self.room_member_repo.get_member(room_id, acting_user_id) if room_id is not None else None
            if room is not None and getattr(room, "role", None) == "leader":
                return await self.message_repo.delete(message_id)
            return None
        except Exception:
            return None

    async def mark_as_read(self, message_id: int, user_id: int) -> Optional[Message]:
        """
        Purpose: Marks a message as read by a user.
        Inputs: message_id (int), user_id (int)
        Outputs: Updated Message object or None.
        """
        try:
            message = await self.message_repo.get_by_id(message_id)
            if not message:
                return None
            setattr(message, "is_read", True)
            try:
                await self.message_repo.db.commit()
                await self.message_repo.db.refresh(message)
            except Exception:
                await self.message_repo.db.rollback()
                return None
            return message
        except Exception:
            return None

    async def edit_message(self, message_id: int, acting_user_id: int, new_content: str) -> Optional[Message]:
        """
        Purpose: Edits a message if the acting user is the sender or room leader.
        Inputs: message_id (int), acting_user_id (int), new_content (str)
        Outputs: Updated Message object or None.
        """
        try:
            message = await self.message_repo.get_by_id(message_id)
            if not message:
                return None
            sender_id = getattr(message, "sender_id", None)
            room_id = getattr(message, "room_id", None)
            room = await self.room_member_repo.get_member(room_id, acting_user_id) if room_id is not None else None
            if sender_id == acting_user_id or (room is not None and getattr(room, "role", None) == "leader"):
                return await self.message_repo.update_message(message_id, new_content)
            return None
        except Exception:
            return None

    async def reply_to_message(self, user_id: int, room_id: int, parent_message_id: int, content: str) -> Optional[Message]:
        """
        Purpose: Creates a reply to a message if the user is permitted.
        Inputs: user_id (int), room_id (int), parent_message_id (int), content (str)
        Outputs: Created reply Message object or None.
        """
        try:
            member = await self.room_member_repo.add_member(room_id, user_id)
            if not member or not getattr(member, "is_permitted", False):
                return None
            parent = await self.message_repo.get_by_id(parent_message_id)
            if not parent or getattr(parent, "room_id", None) != room_id:
                return None
            return await self.message_repo.create_reply(room_id, user_id, parent_message_id, content)
        except Exception:
            return None


class CallService:
    def __init__(self, call_repo: CallRepository, call_participant_repo: CallParticipantRepository, room_member_repo: RoomMemberRepository):
        """
        Purpose: Initializes the CallService with call, participant, and room member repositories.
        Inputs: call_repo, call_participant_repo, room_member_repo
        Outputs: None.
        """
        self.call_repo: CallRepository = call_repo
        self.call_participant_repo: CallParticipantRepository = call_participant_repo
        self.room_member_repo: RoomMemberRepository = room_member_repo

    async def start_call(self, room_id: int, initiator_id: int, call_type: str) -> Optional[Call]:
        """
        Purpose: Starts a new call in a room if the initiator is permitted.
        Inputs: room_id (int), initiator_id (int), call_type (str)
        Outputs: Created Call object or None.
        """
        try:
            member = await self.room_member_repo.add_member(room_id, initiator_id)
            if not member or not getattr(member, "is_permitted", False):
                return None
            call = await self.call_repo.create(room_id=room_id, initiator_id=initiator_id, call_type=call_type)
            call_id_val = getattr(call, 'call_id', None)
            if call_id_val is not None and hasattr(call_id_val, 'value'):
                call_id_val = call_id_val.value
            if not isinstance(call_id_val, int):
                try:
                    call_id_val = int(str(call_id_val))
                except Exception:
                    call_id_val = None
            if call_id_val is not None:
                await self.call_participant_repo.add_participant(call_id_val, initiator_id)
                # Notify channel (real-time system) that call started
                # This is a placeholder for actual channel logic
                try:
                    # Example: channel_module.notify_call_started(room_id, call)
                    pass
                except Exception:
                    pass
            return call
        except Exception:
            return None

    async def join_call(self, call_id: int, user_id: int) -> Optional[CallParticipant]:
        """
        Purpose: Adds a user as a participant to a call if permitted.
        Inputs: call_id (int), user_id (int)
        Outputs: CallParticipant object or None.
        """
        try:
            call = await self.call_repo.get_active_call_by_room(call_id)
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
            member = await self.room_member_repo.add_member(room_id_val, user_id)
            if not member or not getattr(member, "is_permitted", False):
                return None
            participant = await self.call_participant_repo.add_participant(call_id, user_id)
            # Notify channel (real-time system) that user joined call
            try:
                # Example: channel_module.notify_user_joined_call(call_id, user_id)
                pass
            except Exception:
                pass
            return participant
        except Exception:
            return None

    async def leave_call(self, call_id: int, user_id: int) -> Optional[CallParticipant]:
        """
        Purpose: Removes a user from a call's participants.
        Inputs: call_id (int), user_id (int)
        Outputs: CallParticipant object or None.
        """
        try:
            participant = await self.call_participant_repo.remove_participant(call_id, user_id)
            # Notify channel (real-time system) that user left call
            try:
                # Example: channel_module.notify_user_left_call(call_id, user_id)
                pass
            except Exception:
                pass
            return participant
        except Exception:
            return None

    async def end_call(self, call_id: int, acting_user_id: int) -> Optional[Call]:
        """
        Purpose: Ends a call if the acting user is the room leader.
        Inputs: call_id (int), acting_user_id (int)
        Outputs: Ended Call object or None.
        """
        try:
            call = await self.call_repo.get_active_call_by_room(call_id)
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
            room = await self.room_member_repo.get_member(room_id_val, acting_user_id)
            if room is not None and getattr(room, "role", None) == "leader":
                return await self.call_repo.end_call(call_id)
            return None
        except Exception:
            return None

    async def mute_user(self, call_id: int, target_user_id: int, acting_user_id: int) -> Optional[CallParticipant]:
        """
        Purpose: Mutes a user in a call if the acting user is the room leader.
        Inputs: call_id (int), target_user_id (int), acting_user_id (int)
        Outputs: Updated CallParticipant object or None.
        """
        try:
            call = await self.call_repo.get_active_call_by_room(call_id)
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
            room = await self.room_member_repo.get_member(room_id_val, acting_user_id)
            if room is not None and getattr(room, "role", None) == "leader":
                return await self.call_participant_repo.leader_mute(call_id, target_user_id, acting_user_id)
            return None
        except Exception:
            return None

    async def unmute_user(self, call_id: int, target_user_id: int, acting_user_id: int) -> Optional[CallParticipant]:
        """
        Purpose: Unmutes a user in a call if the acting user is the user themselves.
        Inputs: call_id (int), target_user_id (int), acting_user_id (int)
        Outputs: Updated CallParticipant object or None.
        """
        try:
            if acting_user_id != target_user_id:
                return None
            return await self.call_participant_repo.user_unmute(call_id, target_user_id)
        except Exception:
            return None

    async def get_call_state(self, call_id: int) -> Optional[Dict[str, Any]]:
        """
        Purpose: Retrieves the current state of a call, including participants.
        Inputs: call_id (int)
        Outputs: Dict with call and participants, or None.
        """
        try:
            call = await self.call_repo.get_active_call_by_room(call_id)
            if not call:
                return None
            participants = await self.call_participant_repo.get_participants(call_id)
            return {"call": call, "participants": participants}
        except Exception:
            return None