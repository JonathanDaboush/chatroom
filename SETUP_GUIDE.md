# 🔧 Step-by-Step Setup Guide

This guide walks you through setting up the chatroom application from scratch. Follow each step in order.

---

## ⏰ Estimated Time: 20-30 minutes

---

## STEP 1: Install Required Software (10-15 minutes)

### 1.1 Install Python 3.10+

**Windows:**
1. Go to https://www.python.org/downloads/
2. Click "Download Python 3.x.x"
3. Run installer
4. ✅ **IMPORTANT**: Check "Add Python to PATH"
5. Click "Install Now"

**Verify installation:**
```powershell
python --version
```
Should show: `Python 3.10.x` or higher

**macOS:**
```bash
brew install python@3.10
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3.10 python3.10-venv python3-pip
```

---

### 1.2 Install Node.js 18+

**Windows/macOS:**
1. Go to https://nodejs.org/
2. Download LTS version (18.x or higher)
3. Run installer with default settings

**Verify installation:**
```powershell
node --version
npm --version
```

**Linux (Ubuntu/Debian):**
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

---

### 1.3 Install PostgreSQL 12+

**Windows:**
1. Go to https://www.postgresql.org/download/windows/
2. Download installer
3. Run installer
4. **Remember the password you set for 'postgres' user!**
5. Default port: 5432 (keep it)

**macOS:**
```bash
brew install postgresql@14
brew services start postgresql@14
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

**Verify installation:**
```powershell
psql --version
```

---

## STEP 2: Setup Database (2 minutes)

### 2.1 Open PostgreSQL Command Line

**Windows:**
- Search for "SQL Shell (psql)" in Start Menu
- Press Enter 4 times to accept defaults
- Enter your postgres password

**macOS/Linux:**
```bash
psql -U postgres
```

### 2.2 Create Database

In the psql prompt:
```sql
CREATE DATABASE chatroom_db;
```

You should see: `CREATE DATABASE`

### 2.3 Verify Database Created

```sql
\l
```

You should see `chatroom_db` in the list.

### 2.4 Exit psql

```sql
\q
```

---

## STEP 3: Setup Backend (5 minutes)

### 3.1 Open Terminal in Backend Directory

**Windows PowerShell:**
```powershell
cd C:\path\to\chatroom\backend
```

**macOS/Linux:**
```bash
cd /path/to/chatroom/backend
```

### 3.2 Create Virtual Environment

**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

You should see `(venv)` appear in your prompt.

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3.3 Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will take 1-2 minutes. You'll see many packages being installed.

---

### 3.4 Create `.env` File

**Create the file:**

**Windows PowerShell:**
```powershell
New-Item .env -ItemType File
notepad .env
```

**macOS/Linux:**
```bash
touch .env
nano .env
# or use your preferred editor
```

**Copy this content into `.env`:**

```env
# ===================================
# DATABASE CONFIGURATION - CHANGE THIS!
# ===================================
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD_HERE@localhost:5432/chatroom_db

# ===================================
# SECURITY - CHANGE THIS!
# ===================================
SECRET_KEY=CHANGE_ME_TO_A_RANDOM_SECRET_KEY_AT_LEAST_32_CHARACTERS_LONG

# Security Settings (Can keep defaults)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# ===================================
# CORS - Frontend URL
# ===================================
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# ===================================
# EMAIL (OPTIONAL - Leave as-is if not using)
# ===================================
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=
SMTP_PASSWORD=
EMAIL_FROM=

# ===================================
# APPLICATION
# ===================================
APP_NAME=Chatroom
DEBUG=True
```

**⚠️ YOU MUST CHANGE:**

1. **`DATABASE_URL`**: Replace `YOUR_PASSWORD_HERE` with your PostgreSQL password
   
   Example:
   ```env
   DATABASE_URL=postgresql://postgres:mypassword123@localhost:5432/chatroom_db
   ```

2. **`SECRET_KEY`**: Generate a secure key

   **Windows PowerShell:**
   ```powershell
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```
   
   **macOS/Linux:**
   ```bash
   python3 -c "import secrets; print(secrets.token_urlsafe(32))"
   ```
   
   Copy the output (something like `Xa8tB2nC_9dEfGhI-0jKlMnOpQrStUvWxYz1234567`)
   
   Replace `CHANGE_ME_TO_A_RANDOM_SECRET_KEY_AT_LEAST_32_CHARACTERS_LONG` with it.

**Save the file!**

---

### 3.5 Run Database Migrations

Make sure you're still in the `backend` directory with venv activated:

```bash
alembic upgrade head
```

**Expected output:**
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade -> 4051be30b632, initial create all tables
```

✅ **Success!** Database tables are created.

---

### 3.6 Test Backend

Start the backend server:

```bash
uvicorn main:app --reload
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx]
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Test it:**
- Open browser
- Go to `http://localhost:8000/docs`
- You should see the API documentation page

✅ **Success!** Backend is working.

**Keep this terminal open** (or press Ctrl+C to stop for now)

---

## STEP 4: Setup Frontend (3 minutes)

### 4.1 Open NEW Terminal Window

**Keep backend terminal open if running, or you'll need to start it again later**

### 4.2 Navigate to Frontend Directory

**Windows PowerShell:**
```powershell
cd C:\path\to\chatroom\frontend
```

**macOS/Linux:**
```bash
cd /path/to/chatroom/frontend
```

### 4.3 Install Dependencies

```bash
npm install
```

This takes 2-3 minutes. You'll see a progress bar.

---

### 4.4 Create `.env` File

**Create the file:**

**Windows PowerShell:**
```powershell
New-Item .env -ItemType File
notepad .env
```

**macOS/Linux:**
```bash
touch .env
nano .env
```

**Copy this content into `.env`:**

```env
# ===================================
# BACKEND API URL
# ===================================
VITE_API_BASE_URL=http://localhost:8000/api

# ===================================
# WEBSOCKET URL
# ===================================
VITE_WS_BASE_URL=ws://localhost:8000/ws
```

**For local development, you can keep these as-is.**

**For production, change to your actual backend domain:**
```env
VITE_API_BASE_URL=https://your-backend.com/api
VITE_WS_BASE_URL=wss://your-backend.com/ws
```

**Save the file!**

---

### 4.5 Test Frontend

Start the frontend:

```bash
npm run dev
```

**Expected output:**
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
```

✅ **Success!** Frontend is running.

---

## STEP 5: Run the Complete Application

### 5.1 You Need TWO Terminal Windows

**Terminal 1 - Backend:**
```bash
cd chatroom/backend
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux
uvicorn main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd chatroom/frontend
npm run dev
```

---

### 5.2 Access the Application

1. **Open browser**: `http://localhost:3000`

2. **You should see**: Login page

3. **Click**: "Register" link

4. **Fill in**:
   - Username: `testuser`
   - Email: `test@example.com`
   - Password: `password123`
   - Confirm Password: `password123`

5. **Click**: "Register"

6. **You should be**: Redirected to login page

7. **Login** with your credentials

8. **You should see**: The main app with sidebar

✅ **Success!** Application is fully working!

---

## STEP 6: Create Your First Chat Room

1. **In the sidebar**, look for the "+" button next to "Rooms"

2. **Click the "+" button**

3. **Enter room name**: `General`

4. **Click "Create"**

5. **You should see**: The chat interface with message input

6. **Type a message** and press Enter

7. **You should see**: Your message appear in the chat

✅ **Success!** You're ready to chat!

---

## 🎉 You're Done!

The application is now fully set up and running.

---

## 📝 Quick Command Reference

### Start Backend
```bash
cd chatroom/backend
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
uvicorn main:app --reload
```

### Start Frontend
```bash
cd chatroom/frontend
npm run dev
```

### Stop Servers
- Press **Ctrl+C** in each terminal

---

## 🔧 Troubleshooting

### Problem: "Command not found: python"

**Solution:**
```bash
# Try python3 instead
python3 --version

# Or add Python to PATH (Windows)
# Re-run Python installer and check "Add to PATH"
```

---

### Problem: "Permission denied" or "EACCES"

**Solution (macOS/Linux):**
```bash
# Don't use sudo with npm!
# Fix npm permissions:
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.profile
source ~/.profile
```

**Solution (Windows):**
```powershell
# Run PowerShell as Administrator
# Or use Git Bash
```

---

### Problem: "Port 3000 already in use"

**Solution:**

Vite will ask: `Port 3000 is in use, try another? (Y/n)`

Press **Y** and use the new port shown.

Or kill the process:

**Windows:**
```powershell
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

**macOS/Linux:**
```bash
lsof -ti:3000 | xargs kill -9
```

---

### Problem: Database connection failed

**Check PostgreSQL is running:**

**Windows:**
- Open "Services" (search in Start)
- Find "postgresql-x64-14" (or your version)
- Make sure it's "Running"

**macOS:**
```bash
brew services list
# postgresql should show "started"
```

**Linux:**
```bash
sudo systemctl status postgresql
```

**Start PostgreSQL if stopped:**

**Windows:** Right-click service → Start

**macOS:**
```bash
brew services start postgresql@14
```

**Linux:**
```bash
sudo systemctl start postgresql
```

---

### Problem: "Alembic upgrade failed"

**Solution:**

```bash
# Check your DATABASE_URL is correct in backend/.env

# Try resetting (⚠️ This deletes all data!)
alembic downgrade base
alembic upgrade head
```

---

### Problem: Frontend shows "Network Error"

**Check:**

1. ✅ Backend is running on `http://localhost:8000`
2. ✅ `frontend/.env` has correct URL
3. ✅ `backend/.env` has `CORS_ORIGINS=http://localhost:3000`
4. ✅ Both servers restarted after `.env` changes

---

### Still Having Issues?

1. **Check all `.env` files** are created and have correct values
2. **Check both servers are running** in separate terminals
3. **Check PostgreSQL is running**
4. **Clear browser cache** and reload
5. **Check browser console** (F12) for errors
6. **Check terminal output** for error messages

---

## 🎯 Next Steps

- Read [README.md](../README.md) for full documentation
- Check [frontend/ARCHITECTURE.md](../frontend/ARCHITECTURE.md) for frontend details
- Explore the API at `http://localhost:8000/docs`
- Customize the UI in `frontend/src/components/`
- Add features by extending services and components

---

**Happy Coding! 🚀**
