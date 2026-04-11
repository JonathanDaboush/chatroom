import React, { useState, KeyboardEvent } from 'react';
import { messageService } from '@/services';
import './MessageInput.css';

interface MessageInputProps {
  roomId: number;
}

const MessageInput: React.FC<MessageInputProps> = ({ roomId }) => {
  const [text, setText] = useState('');
  const [sending, setSending] = useState(false);

  const handleSend = async () => {
    if (!text.trim() || sending) return;

    setSending(true);
    try {
      await messageService.sendMessage(roomId, { content: text.trim() });
      setText('');
    } catch (err) {
      console.error('Failed to send message:', err);
    } finally {
      setSending(false);
    }
  };

  const handleKeyPress = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="message-input">
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyPress={handleKeyPress}
        placeholder="Type a message..."
        disabled={sending}
        rows={3}
      />
      <button 
        onClick={handleSend} 
        disabled={!text.trim() || sending}
        className="btn-send"
      >
        {sending ? 'Sending...' : 'Send'}
      </button>
    </div>
  );
};

export default MessageInput;
