import React, { useState } from 'react';
import { Message } from '@/types';
import { useAuthStore, useChatStore } from '@/stores';
import { messageService } from '@/services';
import './MessageItem.css';

interface MessageItemProps {
  message: Message;
}

const MessageItem: React.FC<MessageItemProps> = ({ message }) => {
  const { user } = useAuthStore();
  const isOwner = user?.id === message.user_id;
  const [showActions, setShowActions] = useState(false);

  const handleDelete = async () => {
    if (!confirm('Delete this message?')) return;
    
    try {
      await messageService.deleteMessage(message.id);
      useChatStore.getState().deleteMessage(message.room_id, message.id);
    } catch (err) {
      console.error('Failed to delete message:', err);
    }
  };

  const formatTime = (timestamp: string) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div 
      className={`message-item ${isOwner ? 'own-message' : ''}`}
      onMouseEnter={() => setShowActions(true)}
      onMouseLeave={() => setShowActions(false)}
    >
      <div className="message-header">
        <span className="message-username">{message.username || 'Unknown'}</span>
        <span className="message-time">{formatTime(message.timestamp)}</span>
      </div>
      <div className="message-content">
        {message.content}
        {message.edited && <span className="edited-badge">(edited)</span>}
      </div>
      {isOwner && showActions && (
        <div className="message-actions">
          <button className="btn-delete" onClick={handleDelete}>
            Delete
          </button>
        </div>
      )}
    </div>
  );
};

export default MessageItem;
