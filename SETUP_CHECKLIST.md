# ✅ Quick Setup Checklist

Print this page or keep it open as a reference while setting up the chatroom application.

---

## 📋 Pre-Setup (Software Installation)

- [ ] Python 3.10+ installed
  ```bash
  python --version
  ```
  
- [ ] Node.js 18+ installed
  ```bash
  node --version
  npm --version
  ```
  
- [ ] PostgreSQL 12+ installed
  ```bash
  psql --version
  ```
  
- [ ] PostgreSQL is running
  - Windows: Check Services
  - macOS: `brew services list`
  - Linux: `sudo systemctl status postgresql`

---

## 🗄️ Database Setup

- [ ] PostgreSQL database created
  ```sql
  CREATE DATABASE chatroom_db;
  ```
  
- [ ] Can connect to database
  ```bash
  psql -U postgres -d chatroom_db
  ```
  
- [ ] Remember your PostgreSQL password (you'll need it!)

---

## 🔧 Backend Setup

- [ ] Navigate to backend directory
  ```bash
  cd chatroom/backend
  ```

- [ ] Virtual environment created
  ```bash
  python -m venv venv
  ```

- [ ] Virtual environment activated
  ```bash
  .\venv\Scripts\activate  # Windows
  source venv/bin/activate  # macOS/Linux
  ```
  (You should see `(venv)` in prompt)

- [ ] Dependencies installed
  ```bash
  pip install -r requirements.txt
  ```

- [ ] `.env` file created in `backend/` directory

- [ ] `DATABASE_URL` in `.env` has correct password
  ```env
  DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/chatroom_db
  ```

- [ ] `SECRET_KEY` generated and added to `.env`
  ```bash
  python -c "import secrets; print(secrets.token_urlsafe(32))"
  ```

- [ ] All required `.env` variables filled in:
  - [ ] `DATABASE_URL`
  - [ ] `SECRET_KEY`
  - [ ] `CORS_ORIGINS`

- [ ] Database migrations applied
  ```bash
  alembic upgrade head
  ```
  (Should see "Running upgrade" messages)

- [ ] Backend starts without errors
  ```bash
  uvicorn main:app --reload
  ```

- [ ] Can access API docs at `http://localhost:8000/docs`

---

## 🎨 Frontend Setup

- [ ] Navigate to frontend directory
  ```bash
  cd chatroom/frontend
  ```

- [ ] Dependencies installed
  ```bash
  npm install
  ```
  (Takes 2-3 minutes)

- [ ] `.env` file created in `frontend/` directory

- [ ] `.env` has correct backend URLs
  ```env
  VITE_API_BASE_URL=http://localhost:8000/api
  VITE_WS_BASE_URL=ws://localhost:8000/ws
  ```

- [ ] Frontend starts without errors
  ```bash
  npm run dev
  ```

- [ ] Can access frontend at `http://localhost:3000`

---

## 🚀 Running the App

- [ ] Backend server running (Terminal 1)
  ```bash
  cd backend
  .\venv\Scripts\activate
  uvicorn main:app --reload
  ```
  Running at: `http://localhost:8000`

- [ ] Frontend server running (Terminal 2)
  ```bash
  cd frontend
  npm run dev
  ```
  Running at: `http://localhost:3000`

- [ ] Can access frontend in browser

- [ ] Can register new user

- [ ] Can login with registered user

- [ ] Can create a room

- [ ] Can send a message

- [ ] Message appears in chat

---

## 🔍 Verification Tests

### Backend Health Check

- [ ] Visit `http://localhost:8000/docs`
  - Should see Swagger API documentation

- [ ] Visit `http://localhost:8000/redoc`
  - Should see ReDoc API documentation

### Frontend Health Check

- [ ] Visit `http://localhost:3000`
  - Should see login page (not error)

- [ ] Browser console has no errors (F12)

- [ ] Network tab shows successful requests

### Database Health Check

- [ ] Database has tables
  ```bash
  psql -U postgres -d chatroom_db -c "\dt"
  ```
  Should list: users, rooms, messages, calls, etc.

### WebSocket Health Check

- [ ] Send a message in chat
- [ ] Message appears immediately
- [ ] Browser console shows WebSocket connection (not errors)

---

## 🐛 Troubleshooting Checklist

If something doesn't work:

- [ ] Both servers are running
- [ ] PostgreSQL service is running
- [ ] `.env` files exist in correct locations:
  - `chatroom/backend/.env`
  - `chatroom/frontend/.env`
- [ ] Environment variables are filled in (not placeholders)
- [ ] Database password in `DATABASE_URL` is correct
- [ ] `SECRET_KEY` is generated (not default text)
- [ ] Virtual environment is activated (see `(venv)` in prompt)
- [ ] Restarted servers after changing `.env`
- [ ] Cleared browser cache
- [ ] Checked browser console for errors (F12)
- [ ] Checked terminal output for errors
- [ ] No firewall blocking ports 8000 or 3000

---

## 📁 Files to Create

These files don't exist by default - you must create them:

```
✅ chatroom/backend/.env
✅ chatroom/frontend/.env
```

---

## 🔑 Sensitive Information Check

Make sure these are NEVER committed to Git:

- [ ] `.env` files are in `.gitignore`
- [ ] No passwords in code
- [ ] No API keys in code
- [ ] `SECRET_KEY` is secret
- [ ] Database credentials are secure

---

## 📊 Port Usage

Make sure these ports are free:

- [ ] **8000** - Backend API
- [ ] **3000** - Frontend Dev Server
- [ ] **5432** - PostgreSQL (default)

To check if port is in use:

**Windows:**
```powershell
netstat -ano | findstr :8000
```

**macOS/Linux:**
```bash
lsof -ti:8000
```

---

## ⏱️ Time Estimates

- [ ] Software installation: 15-20 minutes
- [ ] Database setup: 2-3 minutes
- [ ] Backend setup: 5-7 minutes
- [ ] Frontend setup: 3-5 minutes
- [ ] First successful run: 1-2 minutes
- [ ] **Total:** ~30 minutes

---

## 🎯 Success Criteria

You're done when:

✅ Backend runs without errors
✅ Frontend runs without errors
✅ Can access `http://localhost:3000`
✅ Can register a new user
✅ Can login
✅ Can create a room
✅ Can send messages
✅ Messages appear in real-time

---

## 📞 Next Steps After Setup

- [ ] Read [README.md](README.md) for full documentation
- [ ] Explore the API at `http://localhost:8000/docs`
- [ ] Read [frontend/ARCHITECTURE.md](frontend/ARCHITECTURE.md)
- [ ] Customize the UI
- [ ] Add your own features

---

## 💡 Pro Tips

✨ **Keep both terminals visible** so you can see logs

✨ **Use browser DevTools** (F12) to debug frontend issues

✨ **Check server logs** in terminal for backend issues

✨ **Save `.env` files securely** - you'll need them every time

✨ **Commit early and often** - but NEVER commit `.env` files

✨ **Test in incognito mode** if you see strange caching issues

---

## 📝 Notes Section

Use this space to write down:
- Your PostgreSQL password: ___________________________
- Your SECRET_KEY (first 10 chars): ___________________________
- Any custom ports you used: ___________________________
- Issues you encountered: ___________________________
- Solutions that worked: ___________________________

---

**Print this checklist or keep it open in a tab while setting up!**

**Good luck! 🚀**
