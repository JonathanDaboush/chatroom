# FastAPI app with HTTP and WebSocket routes for all controllers
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException

# Import all controller functions
from .controller import (
	register_user_controller, login_user_controller, delete_user_controller, get_user_controller, set_status_controller, search_users_controller,
	create_room_controller, request_to_join_controller, respond_to_invite_controller, join_room_controller, leave_room_controller, get_room_controller, list_members_controller, assign_role_controller, kick_user_controller,
	send_message_controller, get_room_messages_controller, delete_message_controller, mark_as_read_controller, edit_message_controller, reply_to_message_controller,
	start_call_controller, join_call_controller, leave_call_controller, end_call_controller, mute_user_controller, unmute_user_controller, get_call_state_controller
)

app = FastAPI()

# User routes
@app.post("/register")
async def register_user(username: str, email: str, password: str):
	user = await register_user_controller(username, email, password)
	if not user:
		raise HTTPException(status_code=400, detail="Registration failed")
	return user

@app.post("/login")
async def login_user(username: str, password: str):
	user = await login_user_controller(username, password)
	if not user:
		raise HTTPException(status_code=401, detail="Login failed")
	return user

@app.delete("/user/{user_id}")
async def delete_user(user_id: int):
	return await delete_user_controller(user_id)

@app.get("/user/{user_id}")
async def get_user(user_id: int):
	return await get_user_controller(user_id)

@app.post("/user/{user_id}/status")
async def set_status(user_id: int, status: str):
	return await set_status_controller(user_id, status)

@app.get("/users/search")
async def search_users(query: str):
	return await search_users_controller(query)

# Room routes
@app.post("/room")
async def create_room(room_name: str, leader_id: int):
	return await create_room_controller(room_name, leader_id)

@app.post("/room/{room_id}/request")
async def request_to_join(room_id: int, user_id: int):
	return await request_to_join_controller(room_id, user_id)

@app.post("/room/{room_id}/invite/response")
async def respond_to_invite(room_id: int, user_id: int, accept: bool):
	return await respond_to_invite_controller(room_id, user_id, accept)

@app.post("/room/{room_id}/join")
async def join_room(room_id: int, user_id: int):
	return await join_room_controller(room_id, user_id)

@app.post("/room/{room_id}/leave")
async def leave_room(room_id: int, user_id: int):
	return await leave_room_controller(room_id, user_id)

@app.get("/room/{room_id}")
async def get_room(room_id: int):
	return await get_room_controller(room_id)

@app.get("/room/{room_id}/members")
async def list_members(room_id: int):
	return await list_members_controller(room_id)

@app.post("/room/{room_id}/assign-role")
async def assign_role(room_id: int, target_user_id: int, role: str, acting_user_id: int):
	return await assign_role_controller(room_id, target_user_id, role, acting_user_id)

@app.post("/room/{room_id}/kick")
async def kick_user(room_id: int, target_user_id: int, acting_user_id: int):
	return await kick_user_controller(room_id, target_user_id, acting_user_id)

# Message routes
@app.post("/message")
async def send_message(user_id: int, room_id: int, content: str):
	return await send_message_controller(user_id, room_id, content)

@app.get("/room/{room_id}/messages")
async def get_room_messages(room_id: int, limit: int = 50, offset: int = 0):
	return await get_room_messages_controller(room_id, limit, offset)

@app.delete("/message/{message_id}")
async def delete_message(message_id: int, acting_user_id: int):
	return await delete_message_controller(message_id, acting_user_id)

@app.post("/message/{message_id}/read")
async def mark_as_read(message_id: int, user_id: int):
	return await mark_as_read_controller(message_id, user_id)

@app.post("/message/{message_id}/edit")
async def edit_message(message_id: int, acting_user_id: int, new_content: str):
	return await edit_message_controller(message_id, acting_user_id, new_content)

@app.post("/message/{message_id}/reply")
async def reply_to_message(user_id: int, room_id: int, parent_message_id: int, content: str):
	return await reply_to_message_controller(user_id, room_id, parent_message_id, content)

# Call routes
@app.post("/call/start")
async def start_call(room_id: int, initiator_id: int, call_type: str):
	return await start_call_controller(room_id, initiator_id, call_type)

@app.post("/call/{call_id}/join")
async def join_call(call_id: int, user_id: int):
	return await join_call_controller(call_id, user_id)

@app.post("/call/{call_id}/leave")
async def leave_call(call_id: int, user_id: int):
	return await leave_call_controller(call_id, user_id)

@app.post("/call/{call_id}/end")
async def end_call(call_id: int, acting_user_id: int):
	return await end_call_controller(call_id, acting_user_id)

@app.post("/call/{call_id}/mute")
async def mute_user(call_id: int, target_user_id: int, acting_user_id: int):
	return await mute_user_controller(call_id, target_user_id, acting_user_id)

@app.post("/call/{call_id}/unmute")
async def unmute_user(call_id: int, target_user_id: int, acting_user_id: int):
	return await unmute_user_controller(call_id, target_user_id, acting_user_id)

@app.get("/call/{call_id}/state")
async def get_call_state(call_id: int):
	return await get_call_state_controller(call_id)

# --- In-memory room manager for WebSocket chat and signaling ---
from typing import Dict, Set

class ConnectionManager:
	def __init__(self):
		self.active_connections: Dict[int, Set[WebSocket]] = {}

	async def connect(self, room_id: int, websocket: WebSocket):
		await websocket.accept()
		if room_id not in self.active_connections:
			self.active_connections[room_id] = set()
		self.active_connections[room_id].add(websocket)

	def disconnect(self, room_id: int, websocket: WebSocket):
		if room_id in self.active_connections:
			self.active_connections[room_id].discard(websocket)
			if not self.active_connections[room_id]:
				del self.active_connections[room_id]

	async def broadcast(self, room_id: int, message: str):
		if room_id in self.active_connections:
			for connection in list(self.active_connections[room_id]):
				try:
					await connection.send_text(message)
				except Exception:
					pass

manager = ConnectionManager()

# WebSocket endpoint for chat and signaling
@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: int):
	await manager.connect(room_id, websocket)
	try:
		while True:
			data = await websocket.receive_text()
			# Broadcast received message to all clients in the room
			await manager.broadcast(room_id, data)
	except WebSocketDisconnect:
		manager.disconnect(room_id, websocket)
