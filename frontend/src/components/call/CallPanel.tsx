import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useCallStore } from '@/stores';
import { callService } from '@/services';
import ParticipantItem from './ParticipantItem';
import './CallPanel.css';

const CallPanel: React.FC = () => {
  const navigate = useNavigate();
  const { activeCall, participants, isMuted, toggleSelfMute, clearCall } = useCallStore();

  if (!activeCall) {
    return null;
  }

  const handleLeaveCall = async () => {
    try {
      await callService.leaveCall(activeCall.id);
      clearCall();
      navigate(-1);
    } catch (err) {
      console.error('Failed to leave call:', err);
    }
  };

  const handleToggleMute = async () => {
    try {
      toggleSelfMute();
      await callService.toggleMute(activeCall.id, !isMuted);
    } catch (err) {
      console.error('Failed to toggle mute:', err);
    }
  };

  return (
    <div className="call-panel">
      <div className="call-header">
        <h2>Active Call</h2>
      </div>

      <div className="participants-list">
        <h3>Participants ({participants.length})</h3>
        {participants.map((participant) => (
          <ParticipantItem key={participant.user.id} participant={participant} />
        ))}
      </div>

      <div className="call-controls">
        <button 
          className={`btn-mute ${isMuted ? 'muted' : ''}`}
          onClick={handleToggleMute}
        >
          {isMuted ? 'Unmute' : 'Mute'}
        </button>
        <button className="btn-leave" onClick={handleLeaveCall}>
          Leave Call
        </button>
      </div>
    </div>
  );
};

export default CallPanel;
