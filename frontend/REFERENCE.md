# Component & File Reference

Quick reference for finding files and understanding their purpose.

## 📁 Core Files

| File | Purpose |
|------|---------|
| `src/main.tsx` | Application entry point |
| `src/App.tsx` | Router configuration |
| `src/App.css` | Global styles |
| `vite.config.ts` | Vite build configuration |
| `tsconfig.json` | TypeScript configuration |

## 🎨 Components

### Layout Components (`src/components/layout/`)

| Component | Purpose | Key Features |
|-----------|---------|--------------|
| `AppLayout.tsx` | Main app wrapper | Auth check, sidebar + content layout |
| `Sidebar.tsx` | Navigation sidebar | Room list, create room, logout |

### Chat Components (`src/components/chat/`)

| Component | Purpose | Props |
|-----------|---------|-------|
| `ChatWindow.tsx` | Chat container | `roomId`, `roomName` |
| `ChatHeader.tsx` | Room header | `roomId`, `roomName` |
| `MessageList.tsx` | Message display | `roomId` |
| `MessageItem.tsx` | Single message | `message: Message` |
| `MessageInput.tsx` | Message composer | `roomId` |

### Call Components (`src/components/call/`)

| Component | Purpose | Props |
|-----------|---------|-------|
| `CallPanel.tsx` | Call UI panel | None (uses stores) |
| `ParticipantItem.tsx` | Participant display | `participant: CallParticipant` |

## 📄 Pages

| Page | Route | Purpose |
|------|-------|---------|
| `LoginPage.tsx` | `/login` | User login form |
| `RegisterPage.tsx` | `/register` | User registration form |
| `RoomsPage.tsx` | `/app/rooms` | Welcome/room selection |
| `RoomPage.tsx` | `/app/room/:id` | Chat interface |
| `CallPage.tsx` | `/app/call/:id` | Voice call interface |

## 🔧 Services (`src/services/`)

### API Services

| Service | Methods | Purpose |
|---------|---------|---------|
| `authService.ts` | `login()`, `register()`, `getMe()` | Authentication API |
| `roomService.ts` | `getRooms()`, `createRoom()`, `joinRoom()`, `leaveRoom()` | Room management |
| `messageService.ts` | `getMessages()`, `sendMessage()`, `updateMessage()`, `deleteMessage()` | Message operations |
| `callService.ts` | `startCall()`, `joinCall()`, `leaveCall()`, `toggleMute()` | Call operations |

### Other Services

| Service | Purpose |
|---------|---------|
| `apiClient.ts` | Axios instance with auth interceptors |
| `websocketService.ts` | WebSocket connection manager |

## 🗄️ Stores (`src/stores/`)

| Store | State | Key Actions |
|-------|-------|-------------|
| `authStore.ts` | user, token, isAuthenticated | `login()`, `logout()`, `loadFromStorage()` |
| `chatStore.ts` | rooms, messages, currentRoomId | `setRooms()`, `addMessage()`, `updateMessage()` |
| `socketStore.ts` | connected, currentRoomSocket | `setSocket()`, `disconnect()` |
| `callStore.ts` | activeCall, participants, isMuted | `setActiveCall()`, `toggleMute()`, `clearCall()` |

## 📦 Types (`src/types/`)

### Main Interfaces

```typescript
User {
  id: number
  username: string
  email: string
  status?: 'online' | 'offline' | 'away'
}

Room {
  id: number
  name: string
  created_at: string
  users?: User[]
}

Message {
  id: number
  room_id: number
  user_id: number
  username?: string
  content: string
  timestamp: string
  edited?: boolean
  reply_to?: number
}

Call {
  id: number
  room_id: number
  participants: User[]
  active: boolean
}

CallParticipant {
  user: User
  muted: boolean
}
```

### WebSocket Types

```typescript
enum WSEventType {
  MESSAGE = 'message'
  UPDATE_MESSAGE = 'update_message'
  DELETE_MESSAGE = 'delete_message'
  USER_JOINED = 'user_joined'
  USER_LEFT = 'user_left'
  CALL_UPDATE = 'call_update'
  TYPING = 'typing'
}

WSEvent<T> {
  type: WSEventType
  payload: T
}
```

## ⚙️ Configuration (`src/config/`)

### Constants (`constants.ts`)

```typescript
// API URLs
API_BASE_URL
WS_BASE_URL

// Local Storage Keys
AUTH_TOKEN_KEY
USER_KEY

// API Endpoints
API_ENDPOINTS {
  LOGIN, REGISTER, ME
  ROOMS, ROOM_BY_ID, JOIN_ROOM, LEAVE_ROOM
  ROOM_MESSAGES, MESSAGE_BY_ID
  START_CALL, JOIN_CALL, LEAVE_CALL, MUTE_CALL
}

// WebSocket Endpoints
WS_ENDPOINTS {
  ROOM
}
```

## 🎨 Styling

### CSS Files

| File | Scope |
|------|-------|
| `src/index.css` | Global reset & base styles |
| `src/App.css` | App-level styles |
| `components/**/*.css` | Component-specific styles |
| `pages/Auth.css` | Shared auth page styles |

### Color Scheme

```css
Primary Blue:    #3498db
Secondary Blue:  #667eea
Dark Background: #2c3e50
Light Gray:      #f8f9fa
Success Green:   #27ae60
Danger Red:      #e74c3c
Muted Gray:      #95a5a6
```

## 🔍 Where to Find...

### Authentication Logic
- **Store**: `src/stores/authStore.ts`
- **Service**: `src/services/authService.ts`
- **Pages**: `src/pages/LoginPage.tsx`, `src/pages/RegisterPage.tsx`

### Message Handling
- **Store**: `src/stores/chatStore.ts`
- **Service**: `src/services/messageService.ts`
- **Components**: `src/components/chat/Message*.tsx`

### WebSocket Logic
- **Service**: `src/services/websocketService.ts`
- **Store**: `src/stores/socketStore.ts`
- **Usage**: `src/pages/RoomPage.tsx` (connects on mount)

### Call Features
- **Store**: `src/stores/callStore.ts`
- **Service**: `src/services/callService.ts`
- **Components**: `src/components/call/*.tsx`
- **Page**: `src/pages/CallPage.tsx`

### Routing
- **Config**: `src/App.tsx`
- **Protected Routes**: `src/components/layout/AppLayout.tsx`

### API Configuration
- **Base URL**: `src/config/constants.ts`
- **Interceptors**: `src/services/apiClient.ts`

## 🛠️ Customization Guide

### Adding a New Page

1. Create in `src/pages/YourPage.tsx`
2. Add route in `src/App.tsx`
3. Link from navigation/sidebar

### Adding a New API Endpoint

1. Add to `src/config/constants.ts`
2. Create/update service in `src/services/`
3. Call from component/page

### Adding a New Store

1. Create in `src/stores/yourStore.ts`
2. Export from `src/stores/index.ts`
3. Use in components with `useYourStore()`

### Modifying Styles

1. Component-specific: Edit `.css` file next to component
2. Global: Edit `src/index.css`
3. Theme colors: Update CSS custom properties

---

This reference makes the codebase easy to navigate and extend!
