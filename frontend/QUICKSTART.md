# Quick Start Guide

## 🚀 Get Running in 3 Steps

### 1️⃣ Install Dependencies

```bash
cd frontend
npm install
```

### 2️⃣ Start Development Server

```bash
npm run dev
```

### 3️⃣ Open Browser

Navigate to: `http://localhost:3000`

---

## 🎯 What You'll See

1. **Login Page** (`/login`)
   - Enter username and password
   - Or click "Register" link

2. **Register Page** (`/register`)
   - Create new account
   - Auto-redirect to login

3. **Rooms Page** (`/app/rooms`)
   - Click "+" in sidebar to create room
   - Click any room to enter

4. **Chat Room** (`/app/room/:id`)
   - Send messages
   - Real-time updates via WebSocket
   - Click "Start Call" for voice chat

---

## 🔧 Configuration

### Default Settings

The app connects to:
- **API**: `http://localhost:8000/api`
- **WebSocket**: `ws://localhost:8000/ws`

### Custom Backend URL

Create `.env` file in `frontend/` directory:

```env
VITE_API_BASE_URL=http://your-backend-url/api
VITE_WS_BASE_URL=ws://your-backend-url/ws
```

---

## 📱 Features Overview

### ✅ Working Features

- **Authentication**
  - Login/Logout
  - Register new users
  - Token persistence

- **Chat**
  - Real-time messaging
  - Create/join rooms
  - Delete messages (own messages)
  - Auto-scroll to latest

- **Calls**
  - Start/join calls
  - Participant list
  - Mute controls

### 🎨 UI/UX

- Clean, modern design
- Responsive layout
- Loading states
- Error messages
- Smooth transitions

---

## 🐛 Common Issues

### Port Already in Use

If port 3000 is taken, Vite will ask to use another port. Just press `y`.

### Backend Not Running

Make sure your backend server is running on `http://localhost:8000`

### WebSocket Connection Failed

Check that:
1. Backend WebSocket endpoint is available
2. No CORS issues
3. Correct URL in `.env`

---

## 📖 Next Steps

1. **Read** [ARCHITECTURE.md](./ARCHITECTURE.md) for detailed docs
2. **Explore** the code in `src/` directory
3. **Customize** styling in `.css` files
4. **Extend** with new features

---

## 🛠️ Development Commands

```bash
# Install dependencies
npm install

# Start dev server (http://localhost:3000)
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

---

## 📚 Project Structure

```
frontend/
├── src/
│   ├── components/    # UI components
│   ├── pages/         # Route pages
│   ├── services/      # API & WebSocket
│   ├── stores/        # State management
│   ├── types/         # TypeScript types
│   └── config/        # Configuration
├── package.json
└── vite.config.ts
```

---

## ✨ Tips

1. **State**: Check Zustand stores in DevTools
2. **API**: Use Network tab to debug calls
3. **WebSocket**: Watch Console for events
4. **Errors**: Always visible in UI, not just console

---

**Happy Coding! 🎉**
