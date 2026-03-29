# channel.py
"""
channel.py: Real-time audio/video signaling for rooms
- Handles WebSocket connections for video/audio calls
- Integrates with RoomService and CallService for permissions
- Routes WebRTC signaling messages (offer/answer/ICE) to peers
- Tracks active participants per room
- Does NOT handle media streaming; that is peer-to-peer via WebRTC
"""


import aioredis
import structlog
from fastapi import WebSocket, WebSocketDisconnect, APIRouter, status
from jose import JWTError, jwt
from slowapi.util import get_remote_address
from slowapi import Limiter
 
from typing import Dict, Any, Optional
from .services import RoomService, CallService
from .repositories import RoomRepository, RoomMemberRepository, UserRepository, CallRepository, CallParticipantRepository
from .database import AsyncSessionLocal




router: APIRouter = APIRouter()
limiter = Limiter(key_func=get_remote_address)
logger = structlog.get_logger()

# Redis connection pool (singleton)
redis_pool = None
# description: allows multiple computers or processes to interact and synchronize state efficiently
async def get_redis():
    """
    Purpose: Creates or returns a singleton Redis connection pool for sharing real-time data.
    Inputs: None
    Outputs: Returns an aioredis connection pool.
    """
    global redis_pool
    if redis_pool is None:
        redis_pool = await aioredis.create_redis_pool("redis://redis:6379/0")
    return redis_pool

# JWT config
# a salting key for encoding and decoding JWT tokens, ensuring that they are secure and cannot be easily forged. In production, this should be a strong, random value and kept secret.
SECRET_KEY = "e5N4BTcGIl4SCfByFuHiDgq0a5BFs8MY5WsTvN2PixL"  # Replace with a secure value in production
ALGORITHM = "HS256"

def verify_jwt(token: str):
    """
    Purpose: Decodes and verifies a JWT token using the secret key and algorithm.
    Inputs: token (str): JWT token string.
    Outputs: Returns the decoded payload (dict) if valid, else None.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


# Dependency injection: instantiate repositories/services with DB session




async def get_services():
    """
    Purpose: Instantiates and returns service objects for room and call management, with database session.
    Inputs: None
    Outputs: Tuple of (RoomService, CallService) instances.
    """
    async with AsyncSessionLocal() as db:
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
    Purpose: Manages active WebSocket connections per room for audio/video calls. Enforces membership and call permissions.
    """

    def __init__(self, room_service: RoomService, call_service: CallService):
        """
        Purpose: Initializes the manager with service dependencies.
        Inputs: room_service, call_service
        Outputs: None.
        """
        self.room_service = room_service
        self.call_service = call_service
        self.connections: Dict[str, Dict[int, WebSocket]] = {}


    async def connect(self, room_link: str, websocket: WebSocket, user_id: int, redis=None) -> None:
        """
        Purpose: Accepts a WebSocket connection, validates user/room, registers user, and handles incoming messages.
        Inputs: room_link (str), websocket (WebSocket), user_id (int), redis (optional)
        Outputs: None.
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
                await self.handle_event(room_link, user_id, data, redis)
        except WebSocketDisconnect:
            logger.info("WebSocket disconnected", user_id=user_id, room_link=room_link)
            await self.disconnect(room_link, user_id)
        except Exception as exc:
            logger.error("WebSocket error", error=str(exc))
            await websocket.close(code=status.WS_1011_INTERNAL_ERROR)

    async def handle_event(self, room_link: str, user_id: int, data: dict[str, Any], redis=None) -> None:
        """
        Purpose: Handles incoming signaling events (offer/answer/ICE), relays to peers, and publishes to Redis.
        Inputs: room_link (str), user_id (int), data (dict), redis (optional)
        Outputs: None.
        """
        action: Optional[str] = data.get("action")
        target_id: Optional[int] = data.get("target")  # peer ID

        if action in ["offer", "answer", "ice-candidate"] and target_id is not None:
            msg = {
                "type": action,
                "from": user_id,
                "data": data.get("data")
            }
            # Publish to Redis for cross-instance delivery
            if redis:
                await redis.publish_json(f"room:{room_link}", msg)
            await self.send_to_user(room_link, target_id, msg)

    async def send_to_user(self, room_link: str, target_id: int, message: dict[str, Any]) -> None:
        """
        Purpose: Sends a signaling message to a specific user in a room.
        Inputs: room_link (str), target_id (int), message (dict)
        Outputs: None.
        """
        room = self.connections.get(room_link, {})
        ws: Optional[WebSocket] = room.get(target_id)
        if ws:
            await ws.send_json(message)

    async def broadcast(self, room_link: str, message: dict[str, Any], exclude: Optional[int] = None, redis=None) -> None:
        """
        Purpose: Broadcasts a message to all users in a room, optionally excluding one, and publishes to Redis.
        Inputs: room_link (str), message (dict), exclude (int, optional), redis (optional)
        Outputs: None.
        """
        room = self.connections.get(room_link, {})
        for uid, ws in room.items():
            if exclude is not None and uid == exclude:
                continue
            await ws.send_json(message)
        # Publish to Redis for cross-instance broadcast
        if redis:
            await redis.publish_json(f"room:{room_link}", message)

    async def disconnect(self, room_link: str, user_id: int) -> None:
        """
        Purpose: Removes a user from a room, notifies others, and updates call participation.
        Inputs: room_link (str), user_id (int)
        Outputs: None.
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
@limiter.limit("10/minute")
async def room_channel(websocket: WebSocket, room_link: str, token: Optional[str] = None):
    """
    Purpose: WebSocket endpoint for room signaling; authenticates user, connects to channel, and manages real-time events.
    Inputs: websocket (WebSocket), room_link (str), token (str, optional)
    Outputs: None (handles WebSocket lifecycle).
    """
    redis = await get_redis()
    # JWT authentication
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    payload = verify_jwt(token)
    if not payload or "user_id" not in payload:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    user_id = payload["user_id"]
    if channel_manager is None:
        await websocket.close(code=1011)
        return
    await channel_manager.connect(room_link, websocket, user_id, redis=redis)