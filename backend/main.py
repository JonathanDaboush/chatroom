

from fastapi import FastAPI, HTTPException, Request, status, Depends
from jose import JWTError, jwt
from slowapi import Limiter
from slowapi.util import get_remote_address
import structlog
import asyncio
import aioredis
from .channel import channel_manager

# Import all controller functions
from .controller import (
	register_user_controller, login_user_controller, delete_user_controller, get_user_controller, set_status_controller, search_users_controller,
	create_room_controller, request_to_join_controller, respond_to_invite_controller, join_room_controller, leave_room_controller, get_room_controller, list_members_controller, assign_role_controller, kick_user_controller,
	send_message_controller, get_room_messages_controller, delete_message_controller, mark_as_read_controller, edit_message_controller, reply_to_message_controller,
	start_call_controller, join_call_controller, leave_call_controller, end_call_controller, mute_user_controller, unmute_user_controller, get_call_state_controller
)


app = FastAPI()


# Redis pub/sub relay for cross-instance WebSocket support
@app.on_event("startup")
async def start_redis_relay():
	pubsub = await aioredis.create_redis("redis://redis:6379/0")
	res = await pubsub.psubscribe("room:*")
	async def relay():
		while await res[0].wait_message():
			msg = await res[0].get_json()
			# Extract room_link from channel name
			channel_name = res[0].name.decode()
			if channel_name.startswith("room:"):
				room_link = channel_name[5:]
				# Relay to all local clients in that room
				if channel_manager:
					await channel_manager.broadcast(room_link, msg)
	asyncio.create_task(relay())
limiter = Limiter(key_func=get_remote_address)
logger = structlog.get_logger()

SECRET_KEY = "your-secret-key"  # Use a secure value in production
ALGORITHM = "HS256"

def verify_jwt(token: str):
	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		return payload
	except JWTError:
		return None

def get_current_user(request: Request):
	token = request.headers.get("Authorization")
	if not token or not token.startswith("Bearer "):
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid token")
	payload = verify_jwt(token[7:])
	if not payload or "user_id" not in payload:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
	return payload["user_id"]

# User routes

@app.post("/register")
@limiter.limit("5/minute")
async def register_user(username: str, email: str, password: str, request: Request):
	logger.info("register_user", username=username, email=email)
	user = await register_user_controller(username, email, password)
	if not user:
		logger.warning("Registration failed", username=username)
		raise HTTPException(status_code=400, detail="Registration failed")
	return user


@app.post("/login")
@limiter.limit("10/minute")
async def login_user(username: str, password: str, request: Request):
	logger.info("login_user", username=username)
	user = await login_user_controller(username, password)
	if not user:
		logger.warning("Login failed", username=username)
		raise HTTPException(status_code=401, detail="Login failed")
	return user


@app.delete("/user/{user_id}")
@limiter.limit("20/minute")
async def delete_user(user_id: int, request: Request, current_user: int = Depends(get_current_user)):
	logger.info("delete_user", user_id=user_id, current_user=current_user)
	return await delete_user_controller(user_id)


@app.get("/user/{user_id}")
@limiter.limit("30/minute")
async def get_user(user_id: int, request: Request, current_user: int = Depends(get_current_user)):
	logger.info("get_user", user_id=user_id, current_user=current_user)
	return await get_user_controller(user_id)


@app.post("/user/{user_id}/status")
@limiter.limit("30/minute")
async def set_status(user_id: int, status: str, request: Request, current_user: int = Depends(get_current_user)):
	logger.info("set_status", user_id=user_id, status=status, current_user=current_user)
	return await set_status_controller(user_id, status)


@app.get("/users/search")
@limiter.limit("30/minute")
async def search_users(query: str, request: Request, current_user: int = Depends(get_current_user)):
	logger.info("search_users", query=query, current_user=current_user)
	return await search_users_controller(query)


# Room routes
@app.post("/room")
@limiter.limit("10/minute")
async def create_room(room_name: str, leader_id: int, request: Request, current_user: int = Depends(get_current_user)):
	logger.info("create_room", room_name=room_name, leader_id=leader_id, current_user=current_user)
	return await create_room_controller(room_name, leader_id)


@app.post("/room/{room_id}/request")
@limiter.limit("20/minute")
async def request_to_join(room_id: int, user_id: int, request: Request, current_user: int = Depends(get_current_user)):
	logger.info("request_to_join", room_id=room_id, user_id=user_id, current_user=current_user)
	return await request_to_join_controller(room_id, user_id)


@app.post("/room/{room_id}/invite/response")
@limiter.limit("20/minute")
async def respond_to_invite(room_id: int, user_id: int, accept: bool, request: Request, current_user: int = Depends(get_current_user)):
	logger.info("respond_to_invite", room_id=room_id, user_id=user_id, accept=accept, current_user=current_user)
	return await respond_to_invite_controller(room_id, user_id, accept)


@app.post("/room/{room_id}/join")
@limiter.limit("20/minute")
async def join_room(room_id: int, user_id: int, request: Request, current_user: int = Depends(get_current_user)):
	logger.info("join_room", room_id=room_id, user_id=user_id, current_user=current_user)
	return await join_room_controller(room_id, user_id)


@app.post("/room/{room_id}/leave")
@limiter.limit("20/minute")
async def leave_room(room_id: int, user_id: int, request: Request, current_user: int = Depends(get_current_user)):
	logger.info("leave_room", room_id=room_id, user_id=user_id, current_user=current_user)
	return await leave_room_controller(room_id, user_id)


@app.get("/room/{room_id}")
@limiter.limit("30/minute")
async def get_room(room_id: int, request: Request, current_user: int = Depends(get_current_user)):
	logger.info("get_room", room_id=room_id, current_user=current_user)
	return await get_room_controller(room_id)


@app.get("/room/{room_id}/members")
@limiter.limit("30/minute")
async def list_members(room_id: int, request: Request, current_user: int = Depends(get_current_user)):
	logger.info("list_members", room_id=room_id, current_user=current_user)
	return await list_members_controller(room_id)


@app.post("/room/{room_id}/assign-role")
@limiter.limit("20/minute")
async def assign_role(room_id: int, target_user_id: int, role: str, acting_user_id: int, request: Request, current_user: int = Depends(get_current_user)):
	logger.info("assign_role", room_id=room_id, target_user_id=target_user_id, role=role, acting_user_id=acting_user_id, current_user=current_user)
	return await assign_role_controller(room_id, target_user_id, role, acting_user_id)


@app.post("/room/{room_id}/kick")
@limiter.limit("20/minute")
async def kick_user(room_id: int, target_user_id: int, acting_user_id: int, request: Request, current_user: int = Depends(get_current_user)):
	logger.info("kick_user", room_id=room_id, target_user_id=target_user_id, acting_user_id=acting_user_id, current_user=current_user)
	return await kick_user_controller(room_id, target_user_id, acting_user_id)


# Message routes
@app.post("/message")
@limiter.limit("30/minute")
async def send_message(user_id: int, room_id: int, content: str, request: Request, current_user: int = Depends(get_current_user)):
	logger.info("send_message", user_id=user_id, room_id=room_id, current_user=current_user)
	return await send_message_controller(user_id, room_id, content)


@app.get("/room/{room_id}/messages")
@limiter.limit("30/minute")
async def get_room_messages(room_id: int, request: Request, limit: int = 50, offset: int = 0, current_user: int = Depends(get_current_user)):
	logger.info("get_room_messages", room_id=room_id, current_user=current_user)
	return await get_room_messages_controller(room_id, limit, offset)


@app.delete("/message/{message_id}")
@limiter.limit("20/minute")
async def delete_message(message_id: int, acting_user_id: int, request: Request, current_user: int = Depends(get_current_user)):
	logger.info("delete_message", message_id=message_id, acting_user_id=acting_user_id, current_user=current_user)
	return await delete_message_controller(message_id, acting_user_id)


@app.post("/message/{message_id}/read")
@limiter.limit("30/minute")
async def mark_as_read(message_id: int, user_id: int, request: Request, current_user: int = Depends(get_current_user)):
	logger.info("mark_as_read", message_id=message_id, user_id=user_id, current_user=current_user)
	return await mark_as_read_controller(message_id, user_id)


@app.post("/message/{message_id}/edit")
@limiter.limit("20/minute")
async def edit_message(message_id: int, acting_user_id: int, new_content: str, request: Request, current_user: int = Depends(get_current_user)):
	logger.info("edit_message", message_id=message_id, acting_user_id=acting_user_id, current_user=current_user)
	return await edit_message_controller(message_id, acting_user_id, new_content)


@app.post("/message/{message_id}/reply")
@limiter.limit("20/minute")
async def reply_to_message(user_id: int, room_id: int, parent_message_id: int, content: str, request: Request, current_user: int = Depends(get_current_user)):
	logger.info("reply_to_message", user_id=user_id, room_id=room_id, parent_message_id=parent_message_id, current_user=current_user)
	return await reply_to_message_controller(user_id, room_id, parent_message_id, content)


# Call routes
@app.post("/call/start")
@limiter.limit("10/minute")
async def start_call(room_id: int, initiator_id: int, call_type: str, request: Request, current_user: int = Depends(get_current_user)):
	logger.info("start_call", room_id=room_id, initiator_id=initiator_id, call_type=call_type, current_user=current_user)
	return await start_call_controller(room_id, initiator_id, call_type)


@app.post("/call/{call_id}/join")
@limiter.limit("20/minute")
async def join_call(call_id: int, user_id: int, request: Request, current_user: int = Depends(get_current_user)):
	logger.info("join_call", call_id=call_id, user_id=user_id, current_user=current_user)
	return await join_call_controller(call_id, user_id)


@app.post("/call/{call_id}/leave")
@limiter.limit("20/minute")
async def leave_call(call_id: int, user_id: int, request: Request, current_user: int = Depends(get_current_user)):
	logger.info("leave_call", call_id=call_id, user_id=user_id, current_user=current_user)
	return await leave_call_controller(call_id, user_id)


@app.post("/call/{call_id}/end")
@limiter.limit("10/minute")
async def end_call(call_id: int, acting_user_id: int, request: Request, current_user: int = Depends(get_current_user)):
	logger.info("end_call", call_id=call_id, acting_user_id=acting_user_id, current_user=current_user)
	return await end_call_controller(call_id, acting_user_id)


@app.post("/call/{call_id}/mute")
@limiter.limit("10/minute")
async def mute_user(call_id: int, target_user_id: int, acting_user_id: int, request: Request, current_user: int = Depends(get_current_user)):
	logger.info("mute_user", call_id=call_id, target_user_id=target_user_id, acting_user_id=acting_user_id, current_user=current_user)
	return await mute_user_controller(call_id, target_user_id, acting_user_id)


@app.post("/call/{call_id}/unmute")
@limiter.limit("10/minute")
async def unmute_user(call_id: int, target_user_id: int, acting_user_id: int, request: Request, current_user: int = Depends(get_current_user)):
	logger.info("unmute_user", call_id=call_id, target_user_id=target_user_id, acting_user_id=acting_user_id, current_user=current_user)
	return await unmute_user_controller(call_id, target_user_id, acting_user_id)


@app.get("/call/{call_id}/state")
@limiter.limit("30/minute")
async def get_call_state(call_id: int, request: Request, current_user: int = Depends(get_current_user)):
	logger.info("get_call_state", call_id=call_id, current_user=current_user)
	return await get_call_state_controller(call_id)


# Health/monitoring endpoint
@app.get("/health")
async def health():
	return {"status": "ok"}
