import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useChatStore } from '@/stores';
import './RoomsPage.css';

const RoomsPage: React.FC = () => {
  const navigate = useNavigate();
  const { rooms } = useChatStore();

  return (
    <div className="rooms-page">
      <div className="rooms-content">
        <h1>Welcome to Chatroom</h1>
        <p>Select a room from the sidebar to start chatting</p>
        
        {rooms.length === 0 && (
          <div className="empty-state">
            <p>No rooms available. Create one to get started!</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default RoomsPage;
