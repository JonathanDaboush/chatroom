// API Configuration
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';
export const WS_BASE_URL = import.meta.env.VITE_WS_BASE_URL || 'ws://localhost:8000/ws';

// Local Storage Keys
export const AUTH_TOKEN_KEY = 'auth_token';
export const USER_KEY = 'user';

// API Endpoints
export const API_ENDPOINTS = {
  // Auth
  LOGIN: '/login',
  REGISTER: '/register',
  ME: '/me',
  
  // Rooms
  ROOMS: '/rooms',
  ROOM_BY_ID: (id: number) => `/rooms/${id}`,
  JOIN_ROOM: (id: number) => `/rooms/${id}/join`,
  LEAVE_ROOM: (id: number) => `/rooms/${id}/leave`,
  
  // Messages
  ROOM_MESSAGES: (roomId: number) => `/rooms/${roomId}/messages`,
  MESSAGE_BY_ID: (id: number) => `/messages/${id}`,
  
  // Calls
  START_CALL: '/calls/start',
  JOIN_CALL: (id: number) => `/calls/${id}/join`,
  LEAVE_CALL: (id: number) => `/calls/${id}/leave`,
  MUTE_CALL: (id: number) => `/calls/${id}/mute`,
};

// WebSocket Endpoints
export const WS_ENDPOINTS = {
  ROOM: (roomId: number) => `/room/${roomId}`,
};
