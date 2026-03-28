# Thin controller: delegates all business logic to services
from .services import UserService, RoomService, MessageService, CallService
from .repositories import (
	UserRepository, RoomRepository, RoomMemberRepository, MessageRepository,
	CallRepository, CallParticipantRepository
)

from .database import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession


# Dependency injection: instantiate repositories/services with async DB session
async def get_services() -> tuple[UserService, RoomService, MessageService, CallService]:
	async with AsyncSessionLocal() as db:  # type: ignore
		db: AsyncSession
		user_repo = UserRepository(db)
		room_repo = RoomRepository(db)
		room_member_repo = RoomMemberRepository(db)
		message_repo = MessageRepository(db)
		call_repo = CallRepository(db)
		call_participant_repo = CallParticipantRepository(db)
		user_service = UserService(user_repo)
		room_service = RoomService(room_repo, room_member_repo, user_repo)
		message_service = MessageService(message_repo, room_member_repo)
		call_service = CallService(call_repo, call_participant_repo, room_member_repo)
		return user_service, room_service, message_service, call_service

# User endpoints (now async)
async def register_user_controller(username: str, email: str, password: str):
	user_service, *_ = await get_services()
	return await user_service.register_user(username, email, password)

async def login_user_controller(username: str, password: str):
	user_service, *_ = await get_services()
	return await user_service.login_user(username, password)

async def delete_user_controller(user_id: int):
	user_service, *_ = await get_services()
	return await user_service.delete_user(user_id)

async def get_user_controller(user_id: int):
	user_service, *_ = await get_services()
	return await user_service.get_user(user_id)

async def set_status_controller(user_id: int, status: str):
	user_service, *_ = await get_services()
	return await user_service.set_status(user_id, status)

async def search_users_controller(query: str):
	user_service, *_ = await get_services()
	return await user_service.search_users(query)

# Room endpoints (async)
async def create_room_controller(room_name: str, leader_id: int):
	_, room_service, _, _ = await get_services()
	return await room_service.create_room(room_name, leader_id)

async def request_to_join_controller(room_id: int, user_id: int):
	_, room_service, _, _ = await get_services()
	return await room_service.request_to_join(room_id, user_id)

async def respond_to_invite_controller(room_id: int, user_id: int, accept: bool):
	_, room_service, _, _ = await get_services()
	return await room_service.respond_to_invite(room_id, user_id, accept)

async def join_room_controller(room_id: int, user_id: int):
	_, room_service, _, _ = await get_services()
	return await room_service.join_room(room_id, user_id)

async def leave_room_controller(room_id: int, user_id: int):
	_, room_service, _, _ = await get_services()
	return await room_service.leave_room(room_id, user_id)

async def get_room_controller(room_id: int):
	_, room_service, _, _ = await get_services()
	return await room_service.get_room(room_id)

async def list_members_controller(room_id: int):
	_, room_service, _, _ = await get_services()
	return await room_service.list_members(room_id)

async def assign_role_controller(room_id: int, target_user_id: int, role: str, acting_user_id: int):
	_, room_service, _, _ = await get_services()
	return await room_service.assign_role(room_id, target_user_id, role, acting_user_id)

async def kick_user_controller(room_id: int, target_user_id: int, acting_user_id: int):
	_, room_service, _, _ = await get_services()
	return await room_service.kick_user(room_id, target_user_id, acting_user_id)

# Message endpoints (async)
async def send_message_controller(user_id: int, room_id: int, content: str):
	*_, message_service, _ = await get_services()
	return await message_service.send_message(user_id, room_id, content)

async def get_room_messages_controller(room_id: int, limit: int = 50, offset: int = 0):
	*_, message_service, _ = await get_services()
	return await message_service.get_room_messages(room_id, limit, offset)

async def delete_message_controller(message_id: int, acting_user_id: int):
	*_, message_service, _ = await get_services()
	return await message_service.delete_message(message_id, acting_user_id)

async def mark_as_read_controller(message_id: int, user_id: int):
	*_, message_service, _ = await get_services()
	return await message_service.mark_as_read(message_id, user_id)

async def edit_message_controller(message_id: int, acting_user_id: int, new_content: str):
	"""Edit a message's content if the acting user is the author or has permission."""
	*_, message_service, _ = await get_services()
	return await message_service.edit_message(message_id, acting_user_id, new_content)

async def reply_to_message_controller(user_id: int, room_id: int, parent_message_id: int, content: str):
	"""Send a threaded reply to a specific message in a room."""
	*_, message_service, _ = await get_services()
	return await message_service.reply_to_message(user_id, room_id, parent_message_id, content)

# Call endpoints (async)
async def start_call_controller(room_id: int, initiator_id: int, call_type: str):
	*_, call_service = await get_services()
	return await call_service.start_call(room_id, initiator_id, call_type)

async def join_call_controller(call_id: int, user_id: int):
	*_, call_service = await get_services()
	return await call_service.join_call(call_id, user_id)

async def leave_call_controller(call_id: int, user_id: int):
	*_, call_service = await get_services()
	return await call_service.leave_call(call_id, user_id)

async def end_call_controller(call_id: int, acting_user_id: int):
	*_, call_service = await get_services()
	return await call_service.end_call(call_id, acting_user_id)

async def mute_user_controller(call_id: int, target_user_id: int, acting_user_id: int):
	*_, call_service = await get_services()
	return await call_service.mute_user(call_id, target_user_id, acting_user_id)

async def unmute_user_controller(call_id: int, target_user_id: int, acting_user_id: int):
	*_, call_service = await get_services()
	return await call_service.unmute_user(call_id, target_user_id, acting_user_id)

async def get_call_state_controller(call_id: int):
	*_, call_service = await get_services()
	return await call_service.get_call_state(call_id)
