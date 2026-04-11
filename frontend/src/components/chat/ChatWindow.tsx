import React from 'react';
import ChatHeader from './ChatHeader';
import MessageList from './MessageList';
import MessageInput from './MessageInput';
import './ChatWindow.css';

interface ChatWindowProps {
  roomId: number;
  roomName: string;
}

const ChatWindow: React.FC<ChatWindowProps> = ({ roomId, roomName }) => {
  return (
    <div className="chat-window">
      <ChatHeader roomId={roomId} roomName={roomName} />
      <MessageList roomId={roomId} />
      <MessageInput roomId={roomId} />
    </div>
  );
};

export default ChatWindow;
