# channel.py
"""
channel.py: Real-time audio/video signaling for rooms
- Handles WebSocket connections for video/audio calls
- Integrates with RoomService and CallService for permissions
- Routes WebRTC signaling messages (offer/answer/ICE) to peers
- Tracks active participants per room
- Does NOT handle media streaming; that is peer-to-peer via WebRTC
"""


from fastapi import WebSocket, WebSocketDisconnect, APIRouter
from typing import Dict, Any, Optional
from backend.services import RoomService, CallService
from backend.repositories import RoomRepository, RoomMemberRepository, UserRepository, CallRepository, CallParticipantRepository
from backend.database import AsyncSessionLocal



router: APIRouter = APIRouter()


# Dependency injection: instantiate repositories/services with DB session



from sqlalchemy.ext.asyncio import AsyncSession

async def get_services():
    async with AsyncSessionLocal() as db:  # type: ignore
        db: AsyncSession  # type hint for Pylance
        room_repo = RoomRepository(db)
        room_member_repo = RoomMemberRepository(db)
        user_repo = UserRepository(db)
        call_repo = CallRepository(db)
        call_participant_repo = CallParticipantRepository(db)
        room_service = RoomService(room_repo=room_repo, room_member_repo=room_member_repo, user_repo=user_repo)
        call_service = CallService(call_repo=call_repo, call_participant_repo=call_participant_repo, room_member_repo=room_member_repo)
        return room_service, call_service

class ChannelManager:
    """
    Manages active WebSocket connections per room for audio/video calls.
    Enforces membership and call permissions.
    """

    def __init__(self, room_service: RoomService, call_service: CallService):
        self.room_service = room_service
        self.call_service = call_service
        self.connections: Dict[str, Dict[int, WebSocket]] = {}

    async def connect(self, room_link: str, websocket: WebSocket, user_id: int) -> None:
        """
        Accept WebSocket connection and register user in room channel.
        Validates room and membership.
        """
        await websocket.accept()

        # Use async repo/service methods
        room = await self.room_service.room_repo.get_by_id_by_link(room_link)
        if not room:
            await websocket.close(code=4004)
            return
        room_id_val = getattr(room, "room_id", None)
        if room_id_val is not None and hasattr(room_id_val, 'value'):
            room_id_val = room_id_val.value
        if not isinstance(room_id_val, int):
            await websocket.close(code=4004)
            return
        member = await self.room_service.room_member_repo.get_member(room_id_val, user_id)
        if not member or not getattr(member, "is_permitted", False):
            await websocket.close(code=4003)
            return
        if room_link not in self.connections:
            self.connections[room_link] = {}
        self.connections[room_link][user_id] = websocket
        await self.broadcast(room_link, {
            "type": "user_joined",
            "user_id": user_id
        }, exclude=user_id)

        # Track call participation (optional)
        latest_call = await self.call_service.call_repo.get_latest_call_by_room(room_id_val)
        if latest_call:
            call_id_val = getattr(latest_call, 'call_id', None)
            if call_id_val is not None and hasattr(call_id_val, 'value'):
                call_id_val = call_id_val.value
            if isinstance(call_id_val, int):
                await self.call_service.join_call(call_id_val, user_id)

        try:
            while True:
                data = await websocket.receive_json()
                await self.handle_event(room_link, user_id, data)
        except WebSocketDisconnect:
            await self.disconnect(room_link, user_id)

    async def handle_event(self, room_link: str, user_id: int, data: dict[str, Any]) -> None:
        """
        Handle incoming signaling messages.
        Supports WebRTC signaling: 'offer', 'answer', 'ice-candidate'.
        """
        action: Optional[str] = data.get("action")
        target_id: Optional[int] = data.get("target")  # peer ID

        if action in ["offer", "answer", "ice-candidate"] and target_id is not None:
            await self.send_to_user(room_link, target_id, {
                "type": action,
                "from": user_id,
                "data": data.get("data")
            })

    async def send_to_user(self, room_link: str, target_id: int, message: dict[str, Any]) -> None:
        """
        Send a signaling message to a specific participant.
        """
        room = self.connections.get(room_link, {})
        ws: Optional[WebSocket] = room.get(target_id)
        if ws:
            await ws.send_json(message)

    async def broadcast(self, room_link: str, message: dict[str, Any], exclude: Optional[int] = None) -> None:
        """
        Broadcast a message to all participants in a room, optionally excluding one.
        """
        room = self.connections.get(room_link, {})
        for uid, ws in room.items():
            if exclude is not None and uid == exclude:
                continue
            await ws.send_json(message)

    async def disconnect(self, room_link: str, user_id: int) -> None:
        """
        Remove user from room channel and notify others.
        """
        room_conns = self.connections.get(room_link)
        if room_conns and user_id in room_conns:
            del room_conns[user_id]
            # Notify remaining participants
            await self.broadcast(room_link, {
                "type": "user_left",
                "user_id": user_id
            })
            # Remove from call participation
            # Find the room object using async repo method
            db_room = await self.room_service.room_repo.get_by_id_by_link(room_link)
            room_id_val = getattr(db_room, "room_id", None) if db_room else None
            if room_id_val is not None and hasattr(room_id_val, 'value'):
                room_id_val = room_id_val.value
            if isinstance(room_id_val, int):
                latest_call = await self.call_service.call_repo.get_latest_call_by_room(room_id_val)
                if latest_call:
                    call_id_val = getattr(latest_call, 'call_id', None)
                    if call_id_val is not None and hasattr(call_id_val, 'value'):
                        call_id_val = call_id_val.value
                    if isinstance(call_id_val, int):
                        await self.call_service.leave_call(call_id_val, user_id)


# Instantiate manager with async services


# ChannelManager is initialized at startup (see below)
channel_manager: Optional[ChannelManager] = None


# NOTE: FastAPI's @router.on_event("startup") is deprecated. Use lifespan event handlers in your main app.
# For now, ensure channel_manager is initialized before handling requests.


@router.websocket("/ws/room/{room_link}")
async def room_channel(websocket: WebSocket, room_link: str, user_id: int):
    if channel_manager is None:
        await websocket.close(code=1011)
        return
    await channel_manager.connect(room_link, websocket, user_id)