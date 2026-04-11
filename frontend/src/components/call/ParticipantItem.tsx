import React from 'react';
import { CallParticipant } from '@/types';
import './ParticipantItem.css';

interface ParticipantItemProps {
  participant: CallParticipant;
}

const ParticipantItem: React.FC<ParticipantItemProps> = ({ participant }) => {
  return (
    <div className="participant-item">
      <div className="participant-info">
        <span className="participant-name">{participant.user.username}</span>
        {participant.muted && (
          <span className="mute-indicator">🔇</span>
        )}
      </div>
    </div>
  );
};

export default ParticipantItem;
