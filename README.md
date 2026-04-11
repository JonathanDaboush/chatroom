# 🚀 Chatroom - Complete Real-Time Chat Application

A full-stack real-time chat application with voice call support, built with FastAPI (Python) backend and React (TypeScript) frontend.

---

## 📚 **NEW TO THIS PROJECT? START HERE!**

This project has comprehensive documentation:

1. **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Step-by-step setup for beginners (RECOMMENDED)
2. **[ENV_CONFIGURATION.md](ENV_CONFIGURATION.md)** - Detailed `.env` file configuration
3. **[DOCS_INDEX.md](DOCS_INDEX.md)** - Complete documentation index
4. **This README** - Full reference and API documentation

**First time users:** Follow [SETUP_GUIDE.md](SETUP_GUIDE.md) for a guided walkthrough.

---

## 📋 Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
  - [Database Setup](#database-setup)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)

---

## ✨ Features

- 🔐 **User Authentication** - Register, login, JWT token-based auth
- 💬 **Real-Time Messaging** - WebSocket-powered instant messaging
- 🏠 **Room-Based Chat** - Create and join multiple chat rooms
- ✏️ **Message Management** - Edit and delete your messages
- 📞 **Voice Calls** - Start and join voice calls in rooms
- 👥 **User Presence** - See who's online
- 🔔 **Real-Time Updates** - Live message updates across all clients
- 📱 **Responsive Design** - Works on desktop and mobile

---

## 🛠️ Technology Stack

### Backend
- **Python 3.10+**
- **FastAPI** - Modern web framework
- **SQLAlchemy** - ORM for database
- **PostgreSQL** - Primary database
- **WebSockets** - Real-time communication
- **JWT** - Authentication tokens
- **Alembic** - Database migrations

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Zustand** - State management
- **React Router** - Navigation
- **Axios** - HTTP client
- **WebSocket API** - Real-time updates

---

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

### Required Software

1. **Python 3.10 or higher**
   - Download: https://www.python.org/downloads/
   - Verify: `python --version`

2. **Node.js 18+ and npm**
   - Download: https://nodejs.org/
   - Verify: `node --version` and `npm --version`

3. **PostgreSQL 12+**
   - Download: https://www.postgresql.org/download/
   - Verify: `psql --version`

4. **Git** (optional, for cloning)
   - Download: https://git-scm.com/

### Optional but Recommended

- **Python Virtual Environment** (venv or conda)
- **PostgreSQL GUI** (pgAdmin, DBeaver, etc.)
- **VS Code** or your preferred IDE

---

## 🔧 Installation & Setup

### Step 1: Clone or Download the Project

```bash
# If using Git
git clone <repository-url>
cd chatroom

# Or download and extract the ZIP file
```

---

### Step 2: Backend Setup

#### 2.1 Navigate to Backend Directory

```bash
# From project root
cd chatroom/backend
```

#### 2.2 Create Python Virtual Environment

**On Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

#### 2.3 Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This installs:
- FastAPI and Uvicorn (web server)
- SQLAlchemy and Psycopg2 (database)
- Alembic (migrations)
- Python-Jose (JWT)
- Passlib (password hashing)
- And more...

#### 2.4 Create Backend Environment File

Create a file named `.env` in the `chatroom/backend/` directory:

```bash
# On Windows PowerShell
New-Item .env

# On macOS/Linux
touch .env
```

**Add the following content to `.env`:**

```env
# Database Configuration
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/chatroom_db

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS (Frontend URL)
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Email Configuration (optional - for password reset)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
EMAIL_FROM=your-email@gmail.com

# Application
APP_NAME=Chatroom
API_VERSION=v1
DEBUG=True
```

**⚠️ IMPORTANT - You MUST Change These:**

1. **`DATABASE_URL`**: Replace `your_password` with your PostgreSQL password
   - Format: `postgresql://username:password@host:port/database_name`
   - Example: `postgresql://postgres:mypassword123@localhost:5432/chatroom_db`

2. **`SECRET_KEY`**: Generate a secure random key:
   ```bash
   # Run this in Python to generate a key
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```
   Copy the output and replace `your-super-secret-key-change-this-in-production-min-32-chars`

3. **Email Settings** (Optional): Only needed if you want password reset via email
   - Use Gmail App Password if using Gmail
   - Or remove these lines if not using email features

---

### Step 3: Database Setup

#### 3.1 Create PostgreSQL Database

**Option A: Using PostgreSQL Command Line**

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE chatroom_db;

# Exit
\q
```

**Option B: Using pgAdmin**

1. Open pgAdmin
2. Right-click "Databases" → "Create" → "Database"
3. Name: `chatroom_db`
4. Click "Save"

#### 3.2 Verify Database Connection

```bash
# From backend directory
python -c "from database import engine; print('Database connected!' if engine else 'Failed')"
```

#### 3.3 Run Database Migrations

```bash
# From backend directory (with venv activated)
alembic upgrade head
```

You should see output like:
```
INFO  [alembic.runtime.migration] Running upgrade -> xxxxx, Initial create all tables
```

This creates all necessary tables (users, rooms, messages, calls, etc.)

---

### Step 4: Frontend Setup

#### 4.1 Navigate to Frontend Directory

```bash
# From project root
cd chatroom/frontend
```

#### 4.2 Install Node Dependencies

```bash
npm install
```

This will take a few minutes and installs React, TypeScript, Vite, and all dependencies.

#### 4.3 Create Frontend Environment File

Create a file named `.env` in the `chatroom/frontend/` directory:

```bash
# On Windows PowerShell
New-Item .env

# On macOS/Linux
touch .env
```

**Add the following content to `.env`:**

```env
VITE_API_BASE_URL=http://localhost:8000/api
VITE_WS_BASE_URL=ws://localhost:8000/ws
```

**⚠️ Change These If:**

- Your backend runs on a different port (default is 8000)
- You're deploying to production (use your actual domain)

**Examples:**

Production:
```env
VITE_API_BASE_URL=https://your-domain.com/api
VITE_WS_BASE_URL=wss://your-domain.com/ws
```

Different backend port:
```env
VITE_API_BASE_URL=http://localhost:5000/api
VITE_WS_BASE_URL=ws://localhost:5000/ws
```

---

## 🚀 Running the Application

### Start Backend Server

```bash
# From chatroom/backend directory (with venv activated)
cd chatroom/backend
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**You should see:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Backend is now running at:** `http://localhost:8000`

**API Documentation available at:**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

### Start Frontend Development Server

**Open a NEW terminal window** (keep backend running)

```bash
# From chatroom/frontend directory
cd chatroom/frontend

npm run dev
```

**You should see:**
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

**Frontend is now running at:** `http://localhost:3000`

---

### Access the Application

1. **Open your browser** and go to: `http://localhost:3000`
2. **Register a new account**:
   - Click "Register" link
   - Fill in username, email, password
   - Submit
3. **Login** with your credentials
4. **Create a room** by clicking the "+" button in the sidebar
5. **Start chatting!**

---

## 📁 Project Structure

```
chatroom/
├── backend/                    # Python FastAPI Backend
│   ├── alembic/               # Database migrations
│   │   └── versions/          # Migration files
│   ├── emailTemplates/        # Email HTML templates
│   ├── tests/                 # Backend tests
│   ├── main.py               # FastAPI app entry point
│   ├── database.py           # Database connection
│   ├── classes.py            # Pydantic models
│   ├── controller.py         # Route handlers
│   ├── services.py           # Business logic
│   ├── repositories.py       # Database operations
│   ├── email.py              # Email service
│   ├── channel.py            # WebSocket management
│   ├── requirements.txt      # Python dependencies
│   ├── alembic.ini          # Alembic configuration
│   └── .env                 # Backend environment variables (CREATE THIS)
│
├── frontend/                  # React TypeScript Frontend
│   ├── src/
│   │   ├── components/       # React components
│   │   │   ├── layout/      # AppLayout, Sidebar
│   │   │   ├── chat/        # Chat UI components
│   │   │   └── call/        # Call UI components
│   │   ├── pages/           # Route pages
│   │   ├── services/        # API & WebSocket services
│   │   ├── stores/          # Zustand state stores
│   │   ├── types/           # TypeScript interfaces
│   │   └── config/          # Configuration
│   ├── public/              # Static assets
│   ├── package.json         # Node dependencies
│   ├── vite.config.ts       # Vite configuration
│   ├── tsconfig.json        # TypeScript config
│   └── .env                 # Frontend environment variables (CREATE THIS)
│
├── .gitignore               # Git ignore file
└── README.md                # This file
```

---

## ⚙️ Configuration

### Backend Configuration Options

Edit `backend/.env` to customize:

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DATABASE_URL` | PostgreSQL connection string | - | ✅ Yes |
| `SECRET_KEY` | JWT signing key (32+ chars) | - | ✅ Yes |
| `ALGORITHM` | JWT algorithm | HS256 | No |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | 30 | No |
| `CORS_ORIGINS` | Allowed frontend URLs | http://localhost:3000 | ✅ Yes |
| `SMTP_SERVER` | Email server | smtp.gmail.com | No |
| `SMTP_PORT` | Email port | 587 | No |
| `SMTP_USERNAME` | Email username | - | No |
| `SMTP_PASSWORD` | Email password | - | No |
| `EMAIL_FROM` | Sender email | - | No |
| `DEBUG` | Debug mode | True | No |

### Frontend Configuration Options

Edit `frontend/.env` to customize:

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `VITE_API_BASE_URL` | Backend API URL | http://localhost:8000/api | ✅ Yes |
| `VITE_WS_BASE_URL` | WebSocket URL | ws://localhost:8000/ws | ✅ Yes |

---

## 🔌 API Documentation

Once the backend is running, visit:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Main Endpoints

#### Authentication
- `POST /api/register` - Create new user
- `POST /api/login` - Login and get token
- `GET /api/me` - Get current user

#### Rooms
- `GET /api/rooms` - List all rooms
- `POST /api/rooms` - Create new room
- `POST /api/rooms/{id}/join` - Join a room
- `POST /api/rooms/{id}/leave` - Leave a room

#### Messages
- `GET /api/rooms/{id}/messages` - Get room messages
- `POST /api/rooms/{id}/messages` - Send message
- `PUT /api/messages/{id}` - Edit message
- `DELETE /api/messages/{id}` - Delete message

#### Calls
- `POST /api/calls/start` - Start a call
- `POST /api/calls/{id}/join` - Join call
- `POST /api/calls/{id}/leave` - Leave call
- `POST /api/calls/{id}/mute` - Toggle mute

#### WebSocket
- `WS /ws/room/{room_id}` - Connect to room for real-time updates

---

## 🌐 Deployment

### Backend Deployment (Production)

#### 1. Update Environment Variables

```env
# backend/.env (PRODUCTION)
DATABASE_URL=postgresql://user:pass@your-db-host:5432/chatroom_db
SECRET_KEY=<GENERATE-NEW-SECURE-KEY>
DEBUG=False
CORS_ORIGINS=https://your-frontend-domain.com
```

#### 2. Install Production Server

```bash
pip install gunicorn
```

#### 3. Run with Gunicorn

```bash
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

#### 4. Popular Deployment Platforms

- **Railway** - Great for FastAPI
- **Render** - Free tier available
- **Heroku** - Easy PostgreSQL integration
- **AWS EC2** - Full control
- **DigitalOcean** - App Platform

### Frontend Deployment (Production)

#### 1. Update Environment Variables

```env
# frontend/.env (PRODUCTION)
VITE_API_BASE_URL=https://your-backend-domain.com/api
VITE_WS_BASE_URL=wss://your-backend-domain.com/ws
```

#### 2. Build for Production

```bash
cd frontend
npm run build
```

This creates a `dist/` folder with static files.

#### 3. Deploy Static Files

Upload the `dist/` folder to:

- **Vercel** - Automatic React deployment
- **Netlify** - Easy static site hosting
- **AWS S3 + CloudFront** - Scalable CDN
- **GitHub Pages** - Free hosting
- **Cloudflare Pages** - Fast global CDN

---

## 🐛 Troubleshooting

### Common Issues & Solutions

#### ❌ Backend won't start

**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```bash
# Activate virtual environment
cd backend
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Reinstall dependencies
pip install -r requirements.txt
```

---

#### ❌ Database connection failed

**Error:** `could not connect to server: Connection refused`

**Solution:**
1. Check PostgreSQL is running:
   ```bash
   # Windows (Services)
   # Check "Services" app for "postgresql-x64-xx"
   
   # macOS
   brew services list
   
   # Linux
   sudo systemctl status postgresql
   ```

2. Verify database exists:
   ```bash
   psql -U postgres -l
   ```

3. Check `DATABASE_URL` in `backend/.env` matches your PostgreSQL setup

---

#### ❌ Alembic migration fails

**Error:** `Target database is not up to date`

**Solution:**
```bash
cd backend

# Reset migrations (WARNING: Destroys data)
alembic downgrade base
alembic upgrade head

# Or create a new migration
alembic revision --autogenerate -m "description"
alembic upgrade head
```

---

#### ❌ Frontend can't connect to backend

**Error:** `Network Error` or CORS error in browser console

**Solution:**

1. Check backend is running:
   - Visit `http://localhost:8000/docs`

2. Check `frontend/.env`:
   ```env
   VITE_API_BASE_URL=http://localhost:8000/api
   VITE_WS_BASE_URL=ws://localhost:8000/ws
   ```

3. Check backend `CORS_ORIGINS` in `backend/.env`:
   ```env
   CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
   ```

4. Restart both servers after changing `.env` files

---

#### ❌ WebSocket connection fails

**Error:** `WebSocket connection failed` in console

**Solution:**

1. Check WebSocket URL in `frontend/.env`:
   ```env
   VITE_WS_BASE_URL=ws://localhost:8000/ws
   ```
   (Note: `ws://` not `http://`)

2. Check browser console for detailed error

3. Try in incognito mode (extensions can block WebSocket)

---

#### ❌ JWT Token invalid

**Error:** `401 Unauthorized` or `Token expired`

**Solution:**

1. Check `SECRET_KEY` in `backend/.env` hasn't changed
2. Clear browser localStorage:
   - Open DevTools → Application → Local Storage → Clear
3. Login again

---

#### ❌ npm install fails

**Error:** `EACCES` or permission errors

**Solution:**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json  # macOS/Linux
# OR manually delete node_modules folder on Windows

npm install
```

---

### Getting Help

If you encounter issues not covered here:

1. **Check the logs**:
   - Backend: Terminal where `uvicorn` is running
   - Frontend: Browser DevTools Console (F12)

2. **Verify all environment variables** are set correctly

3. **Restart both servers** after configuration changes

4. **Check database** has all tables created:
   ```bash
   psql -U postgres -d chatroom_db -c "\dt"
   ```

---

## 📝 Environment Variables Summary

### Quick Reference: What You MUST Change

| File | Variable | What to Change |
|------|----------|----------------|
| `backend/.env` | `DATABASE_URL` | Your PostgreSQL password |
| `backend/.env` | `SECRET_KEY` | Generate secure random key |
| `backend/.env` | `CORS_ORIGINS` | Your frontend URL (production) |
| `frontend/.env` | `VITE_API_BASE_URL` | Your backend URL (production) |
| `frontend/.env` | `VITE_WS_BASE_URL` | Your backend WebSocket URL (production) |

---

## 🎯 Quick Start Checklist

- [ ] Install Python 3.10+
- [ ] Install Node.js 18+
- [ ] Install PostgreSQL 12+
- [ ] Create PostgreSQL database `chatroom_db`
- [ ] Create `backend/.env` with DATABASE_URL and SECRET_KEY
- [ ] Create `frontend/.env` with API URLs
- [ ] Install backend dependencies: `pip install -r requirements.txt`
- [ ] Run migrations: `alembic upgrade head`
- [ ] Install frontend dependencies: `npm install`
- [ ] Start backend: `uvicorn main:app --reload`
- [ ] Start frontend: `npm run dev`
- [ ] Visit `http://localhost:3000` and create account

---

## � Security & Sensitive Information

### .gitignore Configuration

This project includes a comprehensive `.gitignore` file that protects:

✅ **Environment variables** (`.env` files)
✅ **Secret keys and credentials**
✅ **Database files and backups**
✅ **API keys and tokens**
✅ **Virtual environments**
✅ **Node modules**
✅ **Build artifacts**
✅ **IDE configurations**
✅ **Uploaded files**
✅ **Log files**

**⚠️ NEVER commit:**
- `.env` files
- `SECRET_KEY` values
- Database passwords
- API keys or tokens
- SSL certificates
- Private keys

The `.gitignore` is already configured to prevent these from being committed.

### Before Deploying to Production

1. Generate NEW `SECRET_KEY` (different from development)
2. Use strong database passwords
3. Enable HTTPS/WSS
4. Set `DEBUG=False`
5. Review CORS settings
6. Use environment variables instead of `.env` files
7. Enable database backups
8. Set up monitoring and logging

---

## 📄 License

This project is provided as-is for educational purposes.

---

## 🙏 Support

For detailed architecture and component documentation:
- Backend: See code comments in `backend/` files
- Frontend: See `frontend/ARCHITECTURE.md` and `frontend/REFERENCE.md`
- Full Docs: See `DOCS_INDEX.md` for complete documentation index

---

**Happy Chatting! 💬**
