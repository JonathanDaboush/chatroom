# 🔑 Environment Variables Configuration

This document explains **exactly** what needs to be changed in the `.env` files.

---

## 📍 Location of .env Files

You need to create TWO `.env` files:

```
chatroom/
├── backend/
│   └── .env          ← CREATE THIS
└── frontend/
    └── .env          ← CREATE THIS
```

⚠️ **These files do NOT exist by default - you must create them!**

---

## 🔧 Backend `.env` File

**Location:** `chatroom/backend/.env`

### Template

```env
# ===================================
# DATABASE CONFIGURATION
# ===================================
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD_HERE@localhost:5432/chatroom_db

# ===================================
# SECURITY
# ===================================
SECRET_KEY=GENERATE_A_SECRET_KEY_HERE
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# ===================================
# CORS (Frontend URLs)
# ===================================
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# ===================================
# EMAIL (OPTIONAL)
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

---

### What to Change

#### 1. `DATABASE_URL` ✅ REQUIRED

**Format:**
```
postgresql://username:password@host:port/database_name
```

**Default PostgreSQL setup:**
```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/chatroom_db
```

**Replace `YOUR_PASSWORD` with:**
- The password you set when installing PostgreSQL
- The password for the `postgres` user

**Examples:**

If your PostgreSQL password is `mypass123`:
```env
DATABASE_URL=postgresql://postgres:mypass123@localhost:5432/chatroom_db
```

If you created a different user `chatuser` with password `chat456`:
```env
DATABASE_URL=postgresql://chatuser:chat456@localhost:5432/chatroom_db
```

**Common Issues:**
- `@` in password? URL-encode it as `%40`
- `#` in password? URL-encode it as `%23`
- Special chars? URL-encode them: https://www.urlencoder.org/

---

#### 2. `SECRET_KEY` ✅ REQUIRED

**This is used to sign JWT tokens. Must be SECRET and RANDOM!**

**How to Generate:**

Open terminal and run:

**Windows PowerShell:**
```powershell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**macOS/Linux:**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Output (example):**
```
Xa8tB2nC_9dEfGhI-0jKlMnOpQrStUvWxYz1234567
```

**Copy that entire string and paste it:**

```env
SECRET_KEY=Xa8tB2nC_9dEfGhI-0jKlMnOpQrStUvWxYz1234567
```

⚠️ **IMPORTANT:**
- Use a DIFFERENT key for production!
- NEVER commit this to Git!
- Keep it SECRET!
- At least 32 characters long

---

#### 3. `ALGORITHM` - Keep Default

```env
ALGORITHM=HS256
```

✅ No need to change this.

---

#### 4. `ACCESS_TOKEN_EXPIRE_MINUTES` - Optional

```env
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

How long users stay logged in before needing to re-login.

- `30` = 30 minutes (default)
- `60` = 1 hour
- `1440` = 24 hours (1 day)

---

#### 5. `CORS_ORIGINS` - Change for Production

**Local Development (default):**
```env
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

✅ Keep this for local development.

**Production:**
```env
CORS_ORIGINS=https://your-frontend-domain.com,https://www.your-frontend-domain.com
```

**Example:**
```env
CORS_ORIGINS=https://mychat.netlify.app,https://mychat.com
```

⚠️ **Must match your frontend URL exactly!**

---

#### 6. Email Settings - OPTIONAL

**Skip these if you don't need password reset emails.**

If using Gmail:

```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
EMAIL_FROM=your-email@gmail.com
```

**⚠️ For Gmail:**
1. Enable 2-Factor Authentication
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Use the App Password (not your regular password)

**Other email providers:**

| Provider | SMTP Server | Port |
|----------|-------------|------|
| Gmail | smtp.gmail.com | 587 |
| Outlook | smtp-mail.outlook.com | 587 |
| Yahoo | smtp.mail.yahoo.com | 587 |
| SendGrid | smtp.sendgrid.net | 587 |

---

#### 7. `APP_NAME` - Optional

```env
APP_NAME=Chatroom
```

Change to your app's name if you want.

---

#### 8. `DEBUG` - Change for Production

**Development:**
```env
DEBUG=True
```

**Production:**
```env
DEBUG=False
```

When `True`, shows detailed error messages (helpful for debugging).

---

## 🎨 Frontend `.env` File

**Location:** `chatroom/frontend/.env`

### Template

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

---

### What to Change

#### 1. `VITE_API_BASE_URL`

**Local Development (default):**
```env
VITE_API_BASE_URL=http://localhost:8000/api
```

✅ Keep this for local development.

**Production:**
```env
VITE_API_BASE_URL=https://your-backend-domain.com/api
```

**Examples:**

Backend on Railway:
```env
VITE_API_BASE_URL=https://chatroom-backend-production.up.railway.app/api
```

Backend on Render:
```env
VITE_API_BASE_URL=https://chatroom-backend.onrender.com/api
```

Backend on custom domain:
```env
VITE_API_BASE_URL=https://api.mychat.com/api
```

⚠️ **Important:**
- Use `http://` for local
- Use `https://` for production
- Include `/api` at the end

---

#### 2. `VITE_WS_BASE_URL`

**Local Development (default):**
```env
VITE_WS_BASE_URL=ws://localhost:8000/ws
```

✅ Keep this for local development.

**Production:**
```env
VITE_WS_BASE_URL=wss://your-backend-domain.com/ws
```

**Examples:**

```env
VITE_WS_BASE_URL=wss://chatroom-backend.onrender.com/ws
```

⚠️ **Important:**
- Use `ws://` for local (not `http://`)
- Use `wss://` for production (not `https://`)
- Include `/ws` at the end
- Must use same domain as API

---

## 📋 Quick Reference: What MUST Change

### For Local Development

| File | Variable | Change To |
|------|----------|-----------|
| `backend/.env` | `DATABASE_URL` | Your PostgreSQL password |
| `backend/.env` | `SECRET_KEY` | Random generated key |
| `frontend/.env` | `VITE_API_BASE_URL` | ✅ Keep default |
| `frontend/.env` | `VITE_WS_BASE_URL` | ✅ Keep default |

### For Production

| File | Variable | Change To |
|------|----------|-----------|
| `backend/.env` | `DATABASE_URL` | Production database URL |
| `backend/.env` | `SECRET_KEY` | NEW random key (different from dev) |
| `backend/.env` | `CORS_ORIGINS` | Your frontend domain |
| `backend/.env` | `DEBUG` | `False` |
| `frontend/.env` | `VITE_API_BASE_URL` | Your backend domain |
| `frontend/.env` | `VITE_WS_BASE_URL` | Your backend domain (wss://) |

---

## ✅ Validation Checklist

Before running the app, verify:

**Backend `.env`:**
- [ ] `DATABASE_URL` has correct password
- [ ] `DATABASE_URL` ends with `/chatroom_db`
- [ ] `SECRET_KEY` is at least 32 characters
- [ ] `SECRET_KEY` is random (not "CHANGE_ME...")
- [ ] `CORS_ORIGINS` includes `http://localhost:3000`

**Frontend `.env`:**
- [ ] `VITE_API_BASE_URL` ends with `/api`
- [ ] `VITE_WS_BASE_URL` ends with `/ws`
- [ ] `VITE_WS_BASE_URL` starts with `ws://` (not `http://`)

---

## 🧪 Test Your Configuration

### Test Backend `.env`

```bash
cd backend
python -c "from database import engine; print('✅ Database connected!' if engine else '❌ Failed')"
```

Should print: `✅ Database connected!`

### Test Frontend `.env`

```bash
cd frontend
cat .env  # macOS/Linux
type .env  # Windows

# Check the output matches your backend
```

---

## 🔒 Security Best Practices

1. ✅ **NEVER commit `.env` files to Git**
   - They're in `.gitignore` already

2. ✅ **Use different `SECRET_KEY` for dev and production**

3. ✅ **Use environment variables in production**
   - Don't create `.env` files on production servers
   - Use hosting platform's environment variable settings

4. ✅ **Rotate keys regularly** in production

5. ✅ **Use strong database passwords**

---

## 🆘 Common Errors

### "Database connection refused"

**Check:**
```env
DATABASE_URL=postgresql://postgres:PASSWORD@localhost:5432/chatroom_db
                                    ^^^^^^^^
                            Did you change this?
```

### "Invalid token" or "401 Unauthorized"

**Check:**
```env
SECRET_KEY=GENERATE_A_SECRET_KEY_HERE
           ^^^^^^^^^^^^^^^^^^^^^^^^^
           Did you generate a real key?
```

### "CORS error" in browser

**Check backend `.env`:**
```env
CORS_ORIGINS=http://localhost:3000
             ^^^^^^^^^^^^^^^^^^^^^^
             Must match frontend URL
```

### "WebSocket connection failed"

**Check frontend `.env`:**
```env
VITE_WS_BASE_URL=ws://localhost:8000/ws
                 ^^
                 Must be ws:// not http://
```

---

## 📞 Need Help?

If your `.env` files are configured correctly but something still doesn't work:

1. **Restart both servers** after changing `.env` files
2. **Clear browser cache** (Ctrl+Shift+Delete)
3. **Check the console** (F12 in browser)
4. **Check server logs** in the terminal

---

**Remember:** The `.env` files contain sensitive information. Keep them SECRET! 🔒
