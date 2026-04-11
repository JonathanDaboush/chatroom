import { create } from 'zustand';

interface SocketState {
  connected: boolean;
  currentRoomSocket: WebSocket | null;
  
  // Actions
  setConnected: (connected: boolean) => void;
  setSocket: (socket: WebSocket | null) => void;
  disconnect: () => void;
}

export const useSocketStore = create<SocketState>((set, get) => ({
  connected: false,
  currentRoomSocket: null,

  setConnected: (connected) => set({ connected }),

  setSocket: (socket) => set({ 
    currentRoomSocket: socket,
    connected: socket !== null,
  }),

  disconnect: () => {
    const { currentRoomSocket } = get();
    if (currentRoomSocket) {
      currentRoomSocket.close();
      set({ currentRoomSocket: null, connected: false });
    }
  },
}));
