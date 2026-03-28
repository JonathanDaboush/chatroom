from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from backend.database import Base
from datetime import datetime, timezone


class User(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True)
    password_hash = Column(String, nullable=False)
    status = Column(String, default="offline")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    rooms = relationship("RoomMember", back_populates="user")
    messages = relationship("Message", back_populates="sender")
    calls = relationship("CallParticipant", back_populates="user")


class Room(Base):
    __tablename__ = "rooms"
    
    room_id = Column(Integer, primary_key=True, index=True)
    room_name = Column(String, nullable=False)
    leader_id = Column(Integer, ForeignKey("users.user_id"))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    is_active = Column(Boolean, default=True)
    room_link = Column(String, unique=True, nullable=True)  # Unique link for joining/accessing the room

    members = relationship("RoomMember", back_populates="room")
    messages = relationship("Message", back_populates="room")
    calls = relationship("Call", back_populates="room")


class RoomMember(Base):
    __tablename__ = "room_members"
    
    room_member_id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.room_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    joined_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    role = Column(String, default="member")
    # status: 'pending' (invited/requested), 'accepted' (joined), 'rejected' (denied), 'left', 'banned'
    status = Column(String, default="pending")
    is_permitted = Column(Boolean, default=False)
    is_banned = Column(Boolean, default=False)

    # invite_status is now redundant; use status for all transitions
    # Remove invite_status, use status transitions instead

    room = relationship("Room", back_populates="members")
    user = relationship("User", back_populates="rooms")


class Message(Base):
    __tablename__ = "messages"
    
    message_id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.room_id"))
    sender_id = Column(Integer, ForeignKey("users.user_id"))
    content = Column(Text)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    is_read = Column(Boolean, default=False)

    room = relationship("Room", back_populates="messages")
    sender = relationship("User", back_populates="messages")


class Call(Base):
    __tablename__ = "calls"
    
    call_id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.room_id"))
    initiator_id = Column(Integer, ForeignKey("users.user_id"))
    started_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    ended_at = Column(DateTime, nullable=True)
    call_type = Column(String, default="audio")

    room = relationship("Room", back_populates="calls")
    participants = relationship("CallParticipant", back_populates="call")


class CallParticipant(Base):
    __tablename__ = "call_participants"
    
    call_participant_id = Column(Integer, primary_key=True, index=True)
    call_id = Column(Integer, ForeignKey("calls.call_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    joined_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    left_at = Column(DateTime, nullable=True)
    is_muted = Column(Boolean, default=False)

    call = relationship("Call", back_populates="participants")
    user = relationship("User", back_populates="calls")