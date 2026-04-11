export interface User {
  id: number;
  username: string;
  email: string;
  status?: 'online' | 'offline' | 'away';
}

export interface Room {
  id: number;
  name: string;
  created_at: string;
  users?: User[];
}

export interface Message {
  id: number;
  room_id: number;
  user_id: number;
  username?: string;  // Denormalized for easier display
  content: string;
  timestamp: string;
  edited?: boolean;
  reply_to?: number;  // Message ID being replied to
}

export interface Call {
  id: number;
  room_id: number;
  participants: User[];
  active: boolean;
}

export interface CallParticipant {
  user: User;
  muted: boolean;
}

// WebSocket Event Types
export enum WSEventType {
  MESSAGE = 'message',
  UPDATE_MESSAGE = 'update_message',
  DELETE_MESSAGE = 'delete_message',
  USER_JOINED = 'user_joined',
  USER_LEFT = 'user_left',
  CALL_UPDATE = 'call_update',
  TYPING = 'typing',
}

export interface WSEvent<T = any> {
  type: WSEventType;
  payload: T;
}

// API Response Types
export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface CreateRoomRequest {
  name: string;
}

export interface SendMessageRequest {
  content: string;
  reply_to?: number;
}

export interface UpdateMessageRequest {
  content: string;
}

// Input Mode Types
export type MessageInputMode = 'normal' | 'reply' | 'edit';

export interface MessageInputState {
  mode: MessageInputMode;
  targetMessageId?: number;
  targetContent?: string;
}
