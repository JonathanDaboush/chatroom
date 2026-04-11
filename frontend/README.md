# Chatroom Frontend

Modern React chat application with real-time messaging and call functionality.

## Features

- User authentication (login/register)
- Real-time messaging with WebSocket
- Room-based chat
- Voice call interface
- Message editing and deletion
- Responsive design

## Tech Stack

- React 18 with TypeScript
- Vite for build tooling
- Zustand for state management
- React Router for navigation
- Axios for API calls
- WebSocket for real-time communication

## Getting Started

### Installation

```bash
npm install
```

### Development

```bash
npm run dev
```

The app will be available at `http://localhost:3000`

### Build

```bash
npm run build
```

### Preview Production Build

```bash
npm run preview
```

## Project Structure

```
src/
├── components/       # Reusable UI components
│   ├── layout/      # Layout components (AppLayout, Sidebar)
│   ├── chat/        # Chat components (MessageList, MessageInput, etc.)
│   └── call/        # Call components (CallPanel, ParticipantItem)
├── pages/           # Page components
├── services/        # API and WebSocket services
├── stores/          # Zustand state stores
├── types/           # TypeScript type definitions
├── config/          # Configuration files
├── App.tsx          # Main app component with routing
└── main.tsx         # Application entry point
```

## Environment Variables

Create a `.env` file in the root directory:

```env
VITE_API_BASE_URL=http://localhost:8000/api
VITE_WS_BASE_URL=ws://localhost:8000/ws
```

## State Management

The application uses Zustand for state management with the following stores:

- **authStore**: User authentication state
- **chatStore**: Rooms and messages
- **socketStore**: WebSocket connection state
- **callStore**: Active call state

## API Integration

All API calls are handled through service modules in `src/services/`:

- `authService`: Authentication endpoints
- `roomService`: Room management
- `messageService`: Message operations
- `callService`: Call operations
- `websocketService`: Real-time communication

## WebSocket Events

The application listens for the following WebSocket events:

- `message`: New message received
- `update_message`: Message updated
- `delete_message`: Message deleted
- `user_joined`: User joined room
- `user_left`: User left room
- `call_update`: Call state changed

## Contributing

1. Follow the existing code structure
2. Keep business logic separate from components
3. Use TypeScript strictly
4. Test all API integrations
5. Ensure responsive design
