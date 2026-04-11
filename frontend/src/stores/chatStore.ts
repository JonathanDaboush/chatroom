import { create } from 'zustand';
import { Room, Message } from '@/types';

interface ChatState {
  rooms: Room[];
  currentRoomId: number | null;
  messages: Record<number, Message[]>;
  
  // Actions
  setRooms: (rooms: Room[]) => void;
  addRoom: (room: Room) => void;
  setCurrentRoom: (roomId: number | null) => void;
  setMessages: (roomId: number, messages: Message[]) => void;
  addMessage: (roomId: number, message: Message) => void;
  updateMessage: (roomId: number, messageId: number, content: string) => void;
  deleteMessage: (roomId: number, messageId: number) => void;
  clearMessages: (roomId: number) => void;
}

export const useChatStore = create<ChatState>((set) => ({
  rooms: [],
  currentRoomId: null,
  messages: {},

  setRooms: (rooms) => set({ rooms }),

  addRoom: (room) => set((state) => ({
    rooms: [...state.rooms, room],
  })),

  setCurrentRoom: (roomId) => set({ currentRoomId: roomId }),

  setMessages: (roomId, messages) => set((state) => ({
    messages: {
      ...state.messages,
      [roomId]: messages,
    },
  })),

  addMessage: (roomId, message) => set((state) => {
    const roomMessages = state.messages[roomId] || [];
    return {
      messages: {
        ...state.messages,
        [roomId]: [...roomMessages, message],
      },
    };
  }),

  updateMessage: (roomId, messageId, content) => set((state) => {
    const roomMessages = state.messages[roomId] || [];
    return {
      messages: {
        ...state.messages,
        [roomId]: roomMessages.map((msg) =>
          msg.id === messageId ? { ...msg, content, edited: true } : msg
        ),
      },
    };
  }),

  deleteMessage: (roomId, messageId) => set((state) => {
    const roomMessages = state.messages[roomId] || [];
    return {
      messages: {
        ...state.messages,
        [roomId]: roomMessages.filter((msg) => msg.id !== messageId),
      },
    };
  }),

  clearMessages: (roomId) => set((state) => {
    const newMessages = { ...state.messages };
    delete newMessages[roomId];
    return { messages: newMessages };
  }),
}));
