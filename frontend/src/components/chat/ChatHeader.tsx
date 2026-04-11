import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useCallStore } from '@/stores';
import { callService } from '@/services';
import './ChatHeader.css';

interface ChatHeaderProps {
  roomId: number;
  roomName: string;
}

const ChatHeader: React.FC<ChatHeaderProps> = ({ roomId, roomName }) => {
  const navigate = useNavigate();
  const { activeCall, setActiveCall } = useCallStore();

  const handleStartCall = async () => {
    try {
      const call = await callService.startCall(roomId);
      setActiveCall(call);
      navigate(`/app/call/${call.id}`);
    } catch (err) {
      console.error('Failed to start call:', err);
    }
  };

  return (
    <div className="chat-header">
      <div className="chat-header-info">
        <h2>{roomName}</h2>
      </div>
      <div className="chat-header-actions">
        <button 
          className="btn-call"
          onClick={handleStartCall}
          disabled={activeCall !== null}
        >
          {activeCall ? 'Call Active' : 'Start Call'}
        </button>
      </div>
    </div>
  );
};

export default ChatHeader;
