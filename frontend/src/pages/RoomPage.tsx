import React, { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useChatStore } from '@/stores';
import { messageService } from '@/services';
import { wsService } from '@/services/websocketService';
import ChatWindow from '@/components/chat/ChatWindow';

const RoomPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { rooms, setMessages, setCurrentRoom } = useChatStore();
  
  const roomId = id ? parseInt(id, 10) : null;
  const room = rooms.find(r => r.id === roomId);

  useEffect(() => {
    if (!roomId) {
      navigate('/app/rooms');
      return;
    }

    // Set current room
    setCurrentRoom(roomId);

    // Load messages
    const loadMessages = async () => {
      try {
        const messages = await messageService.getMessages(roomId);
        setMessages(roomId, messages);
      } catch (err) {
        console.error('Failed to load messages:', err);
      }
    };

    loadMessages();

    // Connect WebSocket
    wsService.connect(roomId);

    // Cleanup on unmount
    return () => {
      wsService.disconnect();
      setCurrentRoom(null);
    };
  }, [roomId, setMessages, setCurrentRoom, navigate]);

  if (!roomId || !room) {
    return (
      <div style={{ padding: '20px' }}>
        <p>Room not found</p>
      </div>
    );
  }

  return <ChatWindow roomId={roomId} roomName={room.name} />;
};

export default RoomPage;
