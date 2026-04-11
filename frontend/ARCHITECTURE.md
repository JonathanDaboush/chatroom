# Chatroom Frontend - Complete Setup & Architecture Guide

## 🎯 Project Overview

A modern, production-ready React chat application with real-time messaging and call functionality, built according to the provided specification.

## 📋 What Was Built

### ✅ Complete Feature Set

1. **Authentication System**
   - Login page with form validation
   - Register page with password confirmation
   - JWT token management
   - Auto-login from localStorage
   - Protected routes

2. **Real-time Chat**
   - WebSocket integration for instant messaging
   - Message list with auto-scroll
   - Send, edit, and delete messages
   - User-specific message styling
   - Timestamp display

3. **Room Management**
   - Create new rooms
   - Join/leave rooms
   - Room list in sidebar
   - Active room highlighting

4. **Call Functionality**
   - Start/join calls
   - Participant list
   - Mute/unmute controls
   - Leave call functionality

5. **State Management**
   - Zustand stores for all state
   - Centralized business logic
   - Persistent authentication

## 🏗️ Architecture

### Directory Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── layout/
│   │   │   ├── AppLayout.tsx          # Main app wrapper
│   │   │   ├── Sidebar.tsx            # Room list & navigation
│   │   ├── chat/
│   │   │   ├── ChatWindow.tsx         # Chat container
│   │   │   ├── ChatHeader.tsx         # Room header with actions
│   │   │   ├── MessageList.tsx        # Scrollable message list
│   │   │   ├── MessageItem.tsx        # Individual message
│   │   │   └── MessageInput.tsx       # Message composition
│   │   └── call/
│   │       ├── CallPanel.tsx          # Call UI panel
│   │       └── ParticipantItem.tsx    # Participant display
│   ├── pages/
│   │   ├── LoginPage.tsx              # /login
│   │   ├── RegisterPage.tsx           # /register
│   │   ├── RoomsPage.tsx              # /app/rooms
│   │   ├── RoomPage.tsx               # /app/room/:id
│   │   └── CallPage.tsx               # /app/call/:id
│   ├── services/
│   │   ├── apiClient.ts               # Axios instance with interceptors
│   │   ├── authService.ts             # Auth API calls
│   │   ├── roomService.ts             # Room API calls
│   │   ├── messageService.ts          # Message API calls
│   │   ├── callService.ts             # Call API calls
│   │   └── websocketService.ts        # WebSocket management
│   ├── stores/
│   │   ├── authStore.ts               # User authentication state
│   │   ├── chatStore.ts               # Rooms & messages state
│   │   ├── socketStore.ts             # WebSocket connection state
│   │   └── callStore.ts               # Active call state
│   ├── types/
│   │   └── index.ts                   # TypeScript interfaces
│   ├── config/
│   │   └── constants.ts               # API endpoints & config
│   ├── App.tsx                        # Router setup
│   └── main.tsx                       # Entry point
├── package.json
├── tsconfig.json
├── vite.config.ts
└── README.md
```

### State Management (Zustand Stores)

#### authStore
```typescript
- user: User | null
- token: string | null
- isAuthenticated: boolean
- login(user, token)
- logout()
- setUser(user)
- loadFromStorage()
```

#### chatStore
```typescript
- rooms: Room[]
- currentRoomId: number | null
- messages: Record<number, Message[]>
- setRooms(rooms)
- addRoom(room)
- setCurrentRoom(roomId)
- setMessages(roomId, messages)
- addMessage(roomId, message)
- updateMessage(roomId, messageId, content)
- deleteMessage(roomId, messageId)
```

#### socketStore
```typescript
- connected: boolean
- currentRoomSocket: WebSocket | null
- setConnected(connected)
- setSocket(socket)
- disconnect()
```

#### callStore
```typescript
- activeCall: Call | null
- participants: CallParticipant[]
- mutedUsers: Set<number>
- isMuted: boolean
- setActiveCall(call)
- setParticipants(participants)
- toggleMute(userId)
- toggleSelfMute()
- clearCall()
```

### API Service Layer

All API calls are centralized in service modules:

```typescript
// authService
- login(credentials) → LoginResponse
- register(data) → User
- getMe() → User

// roomService
- getRooms() → Room[]
- createRoom(data) → Room
- joinRoom(roomId) → void
- leaveRoom(roomId) → void

// messageService
- getMessages(roomId) → Message[]
- sendMessage(roomId, data) → Message
- updateMessage(messageId, data) → Message
- deleteMessage(messageId) → void

// callService
- startCall(roomId) → Call
- joinCall(callId) → void
- leaveCall(callId) → void
- toggleMute(callId, muted) → void
```

### WebSocket Integration

The `websocketService` handles real-time communication:

**Features:**
- Auto-reconnect with exponential backoff
- Event-based message handling
- Automatic state updates via stores
- Connection state management

**Supported Events:**
- `message` - New message received
- `update_message` - Message edited
- `delete_message` - Message deleted
- `user_joined` - User joined room
- `user_left` - User left room
- `call_update` - Call state changed
- `typing` - User typing indicator

## 🚀 Getting Started

### Step 1: Install Dependencies

```bash
cd frontend
npm install
```

### Step 2: Configure Environment

Create a `.env` file:

```env
VITE_API_BASE_URL=http://localhost:8000/api
VITE_WS_BASE_URL=ws://localhost:8000/ws
```

### Step 3: Run Development Server

```bash
npm run dev
```

The app will be available at `http://localhost:3000`

### Step 4: Build for Production

```bash
npm run build
npm run preview
```

## 🔄 User Flows

### Login Flow
1. User visits `/login`
2. Enters credentials
3. On success: Token stored in localStorage
4. Redirected to `/app/rooms`
5. authStore updated with user data

### Room & Chat Flow
1. User sees room list in sidebar
2. Clicks room → Navigate to `/app/room/:id`
3. RoomPage loads:
   - Fetches message history
   - Connects WebSocket
   - Displays ChatWindow
4. User sends message:
   - API call to create message
   - WebSocket broadcasts to all users
   - Message appears in real-time

### Call Flow
1. User clicks "Start Call" in chat header
2. API creates call
3. Navigate to `/app/call/:id`
4. CallPanel displays participants
5. User can mute/unmute
6. Leave call returns to chat

## 🎨 Design Patterns

### Component Separation
- **Presentational components**: Display data, handle UI
- **Container components**: Connect to stores, manage logic
- **Service layer**: API calls isolated from components

### State Management Rules
1. No business logic in components
2. All API calls go through services
3. State centralized in Zustand stores
4. WebSocket doesn't live in UI components

### Performance Optimizations
- Auto-scroll only when needed
- Memoized message list (can be enhanced)
- Optimistic UI updates
- Lazy loading of messages (can be added)

## 🔌 API Contract

The frontend expects these backend endpoints:

### Authentication
```
POST /api/login
POST /api/register
GET  /api/me
```

### Rooms
```
GET  /api/rooms
POST /api/rooms
POST /api/rooms/:id/join
POST /api/rooms/:id/leave
```

### Messages
```
GET    /api/rooms/:id/messages
POST   /api/rooms/:id/messages
PUT    /api/messages/:id
DELETE /api/messages/:id
```

### Calls
```
POST /api/calls/start
POST /api/calls/:id/join
POST /api/calls/:id/leave
POST /api/calls/:id/mute
```

### WebSocket
```
WS /ws/room/:roomId
```

## 🛠️ Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **React Router 6** - Navigation
- **Zustand** - State management
- **Axios** - HTTP client
- **WebSocket API** - Real-time communication

## 📝 Key Implementation Details

### Authentication
- JWT token stored in localStorage
- Axios interceptor adds token to all requests
- Auto-logout on 401 responses
- Protected routes via AppLayout

### Real-time Messaging
- WebSocket connects when entering room
- Disconnects when leaving
- Auto-reconnect on connection loss
- Events automatically update chatStore

### Form Handling
- Controlled inputs
- Loading states
- Error display
- Validation

### Routing
```
/login               → LoginPage
/register            → RegisterPage
/app                 → AppLayout (wrapper)
  /app/rooms         → RoomsPage
  /app/room/:id      → RoomPage
  /app/call/:id      → CallPage
```

## 🚧 Future Enhancements

1. **Message Features**
   - Reply functionality
   - Edit inline
   - File uploads
   - Link previews
   - Emoji picker

2. **Performance**
   - Virtual scrolling for large message lists
   - Message pagination
   - Image lazy loading
   - Component memoization

3. **UX Improvements**
   - Typing indicators
   - Read receipts
   - Online status
   - Push notifications

4. **Call Features**
   - WebRTC video/audio
   - Screen sharing
   - Call history

## 🔍 Troubleshooting

### WebSocket won't connect
- Check `VITE_WS_BASE_URL` in .env
- Ensure backend WebSocket server is running
- Check browser console for errors

### API calls fail
- Verify `VITE_API_BASE_URL` in .env
- Check backend is running on correct port
- Inspect network tab for errors

### Auth issues
- Clear localStorage
- Check token expiration
- Verify backend auth endpoints

## ✅ Checklist - What's Implemented

- [x] React + TypeScript setup
- [x] Vite build configuration
- [x] React Router navigation
- [x] Zustand state management
- [x] Authentication pages (Login/Register)
- [x] Protected routes
- [x] Room list sidebar
- [x] Create/join rooms
- [x] Real-time chat with WebSocket
- [x] Message send/edit/delete
- [x] Call UI with participants
- [x] Mute controls
- [x] API service layer
- [x] TypeScript interfaces
- [x] Error handling
- [x] Loading states
- [x] Responsive CSS
- [x] Auto-scroll messages
- [x] JWT token management
- [x] Environment configuration

## 📦 Production Deployment

### Build
```bash
npm run build
```

### Deploy
The `dist` folder contains static files that can be deployed to:
- Vercel
- Netlify
- AWS S3 + CloudFront
- GitHub Pages
- Any static hosting

### Environment Variables
Set these in your hosting platform:
- `VITE_API_BASE_URL`
- `VITE_WS_BASE_URL`

---

**The frontend is complete and production-ready!** 🎉

All components follow the specification, state is properly managed, and the architecture is clean and scalable.
