import { WS_BASE_URL, WS_ENDPOINTS } from '@/config/constants';
import { WSEvent, WSEventType, Message } from '@/types';
import { useSocketStore } from '@/stores/socketStore';
import { useChatStore } from '@/stores/chatStore';

type MessageHandler = (event: WSEvent) => void;

class WebSocketService {
  private socket: WebSocket | null = null;
  private roomId: number | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000;
  private handlers: Map<WSEventType, MessageHandler[]> = new Map();

  connect(roomId: number): void {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      if (this.roomId === roomId) {
        console.log('Already connected to this room');
        return;
      }
      this.disconnect();
    }

    this.roomId = roomId;
    const wsUrl = `${WS_BASE_URL}${WS_ENDPOINTS.ROOM(roomId)}`;
    
    console.log('Connecting to WebSocket:', wsUrl);
    this.socket = new WebSocket(wsUrl);

    this.socket.onopen = () => {
      console.log('WebSocket connected');
      this.reconnectAttempts = 0;
      useSocketStore.getState().setSocket(this.socket);
    };

    this.socket.onmessage = (event) => {
      try {
        const wsEvent: WSEvent = JSON.parse(event.data);
        this.handleMessage(wsEvent);
      } catch (error) {
        console.error('Failed to parse WebSocket message:', error);
      }
    };

    this.socket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    this.socket.onclose = () => {
      console.log('WebSocket closed');
      useSocketStore.getState().setSocket(null);
      this.attemptReconnect();
    };
  }

  disconnect(): void {
    if (this.socket) {
      this.socket.close();
      this.socket = null;
      this.roomId = null;
      useSocketStore.getState().setSocket(null);
    }
  }

  send(event: WSEvent): void {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify(event));
    } else {
      console.error('WebSocket is not connected');
    }
  }

  on(eventType: WSEventType, handler: MessageHandler): void {
    if (!this.handlers.has(eventType)) {
      this.handlers.set(eventType, []);
    }
    this.handlers.get(eventType)!.push(handler);
  }

  off(eventType: WSEventType, handler: MessageHandler): void {
    const handlers = this.handlers.get(eventType);
    if (handlers) {
      const index = handlers.indexOf(handler);
      if (index > -1) {
        handlers.splice(index, 1);
      }
    }
  }

  private handleMessage(event: WSEvent): void {
    console.log('WebSocket event received:', event);

    // Default handlers for common events
    const chatStore = useChatStore.getState();
    
    switch (event.type) {
      case WSEventType.MESSAGE:
        if (this.roomId !== null) {
          chatStore.addMessage(this.roomId, event.payload as Message);
        }
        break;
        
      case WSEventType.UPDATE_MESSAGE:
        if (this.roomId !== null && event.payload) {
          const { message_id, content } = event.payload;
          chatStore.updateMessage(this.roomId, message_id, content);
        }
        break;
        
      case WSEventType.DELETE_MESSAGE:
        if (this.roomId !== null && event.payload) {
          chatStore.deleteMessage(this.roomId, event.payload.message_id);
        }
        break;
        
      case WSEventType.USER_JOINED:
      case WSEventType.USER_LEFT:
      case WSEventType.CALL_UPDATE:
      case WSEventType.TYPING:
        // These will be handled by registered handlers
        break;
    }

    // Call registered handlers
    const handlers = this.handlers.get(event.type);
    if (handlers) {
      handlers.forEach((handler) => handler(event));
    }
  }

  private attemptReconnect(): void {
    if (this.reconnectAttempts < this.maxReconnectAttempts && this.roomId !== null) {
      this.reconnectAttempts++;
      const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);
      
      console.log(`Attempting to reconnect in ${delay}ms (attempt ${this.reconnectAttempts})`);
      
      setTimeout(() => {
        if (this.roomId !== null) {
          this.connect(this.roomId);
        }
      }, delay);
    } else {
      console.error('Max reconnect attempts reached');
    }
  }
}

// Export singleton instance
export const wsService = new WebSocketService();
