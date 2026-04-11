import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore, useChatStore } from '@/stores';
import { roomService } from '@/services';
import './Sidebar.css';

const Sidebar: React.FC = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuthStore();
  const { rooms, setRooms, currentRoomId, setCurrentRoom } = useChatStore();
  const [showCreateRoom, setShowCreateRoom] = useState(false);
  const [newRoomName, setNewRoomName] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    loadRooms();
  }, []);

  const loadRooms = async () => {
    try {
      const data = await roomService.getRooms();
      setRooms(data);
    } catch (err) {
      console.error('Failed to load rooms:', err);
    }
  };

  const handleCreateRoom = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newRoomName.trim()) return;

    setLoading(true);
    setError('');

    try {
      const room = await roomService.createRoom({ name: newRoomName });
      await roomService.joinRoom(room.id);
      await loadRooms();
      setNewRoomName('');
      setShowCreateRoom(false);
      navigate(`/app/room/${room.id}`);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create room');
    } finally {
      setLoading(false);
    }
  };

  const handleRoomClick = async (roomId: number) => {
    try {
      await roomService.joinRoom(roomId);
      setCurrentRoom(roomId);
      navigate(`/app/room/${roomId}`);
    } catch (err) {
      console.error('Failed to join room:', err);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h2>Chatroom</h2>
        <div className="user-info">
          <span>{user?.username}</span>
        </div>
      </div>

      <div className="sidebar-content">
        <div className="rooms-header">
          <h3>Rooms</h3>
          <button
            className="btn-create-room"
            onClick={() => setShowCreateRoom(!showCreateRoom)}
          >
            +
          </button>
        </div>

        {showCreateRoom && (
          <form className="create-room-form" onSubmit={handleCreateRoom}>
            <input
              type="text"
              placeholder="Room name"
              value={newRoomName}
              onChange={(e) => setNewRoomName(e.target.value)}
              disabled={loading}
            />
            <div className="form-actions">
              <button type="submit" disabled={loading}>
                Create
              </button>
              <button type="button" onClick={() => setShowCreateRoom(false)}>
                Cancel
              </button>
            </div>
            {error && <div className="error">{error}</div>}
          </form>
        )}

        <div className="rooms-list">
          {rooms.map((room) => (
            <div
              key={room.id}
              className={`room-item ${currentRoomId === room.id ? 'active' : ''}`}
              onClick={() => handleRoomClick(room.id)}
            >
              <div className="room-name">{room.name}</div>
            </div>
          ))}
        </div>
      </div>

      <div className="sidebar-footer">
        <button className="btn-logout" onClick={handleLogout}>
          Logout
        </button>
      </div>
    </div>
  );
};

export default Sidebar;
