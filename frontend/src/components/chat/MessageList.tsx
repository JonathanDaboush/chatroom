import React, { useEffect, useRef } from 'react';
import { useChatStore } from '@/stores';
import MessageItem from './MessageItem';
import './MessageList.css';

interface MessageListProps {
  roomId: number;
}

const MessageList: React.FC<MessageListProps> = ({ roomId }) => {
  const { messages } = useChatStore();
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const roomMessages = messages[roomId] || [];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [roomMessages]);

  if (roomMessages.length === 0) {
    return (
      <div className="message-list">
        <div className="no-messages">
          No messages yet. Start the conversation!
        </div>
      </div>
    );
  }

  return (
    <div className="message-list">
      {roomMessages.map((message) => (
        <MessageItem key={message.id} message={message} />
      ))}
      <div ref={messagesEndRef} />
    </div>
  );
};

export default MessageList;
